# INTEGRATION.md — Cara Memuat Data Meridian Tycoon dalam Android (Kotlin)

Semua fail di `game-data/` ialah JSON UTF-8 tanpa logik. Salin **terus** ke
`app/src/main/assets/data/` (termasuk subfolder `i18n/`). Teks pemain tidak
disimpan dalam fail data — hanya **kunci** yang merujuk `i18n/{en,ms,id}.json`.

```
app/src/main/assets/data/
├── balance.json
├── tiers.json
├── sectors.json
├── operations.json
├── companies.json
├── ai_ceos.json
├── staff_roles.json
├── staff_pool.json
├── research.json
├── events.json
├── seasons.json
├── cosmetics.json
├── milestones.json
├── tutorial.json
├── leaderboard_bots.json
└── i18n/{en,ms,id}.json
```

## 1. Persediaan kotlinx.serialization

```kotlin
// build.gradle.kts (module)
plugins { id("org.jetbrains.kotlin.plugin.serialization") }
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
}
```

Data class sedia-guna ada dalam `Models.kt` (akar repo). Struktur umum:
fail yang "senarai" dibungkus objek supaya setiap fail membawa `dataVersion`:

```json
{ "dataVersion": "1.0.0", "companies": [ ... ] }
```

## 2. Pemuat generik

```kotlin
object GameDataRepo {
    private val json = Json { ignoreUnknownKeys = true }

    private inline fun <reified T> load(context: Context, path: String): T =
        json.decodeFromString(
            T::class.serializer(),
            context.assets.open("data/$path").bufferedReader().use { it.readText() }
        )

    fun loadAll(context: Context): GameData = GameData(
        balance        = load<BalanceFile>(context, "balance.json"),
        tiers          = load<TiersFile>(context, "tiers.json").tiers,
        sectors        = load<SectorsFile>(context, "sectors.json").sectors,
        operations     = load<OperationsFile>(context, "operations.json").operations,
        companies      = load<CompaniesFile>(context, "companies.json").companies,
        ceos           = load<AiCeosFile>(context, "ai_ceos.json").ceos,
        staffRoles     = load<StaffRolesFile>(context, "staff_roles.json").roles,
        staffPool      = load<StaffPoolFile>(context, "staff_pool.json").staff,
        research       = load<ResearchFile>(context, "research.json").nodes,
        events         = load<EventsFile>(context, "events.json"),
        seasons        = load<SeasonsFile>(context, "seasons.json").seasons,
        cosmetics      = load<CosmeticsFile>(context, "cosmetics.json").cosmetics,
        milestones     = load<MilestonesFile>(context, "milestones.json").milestones,
        tutorial       = load<TutorialFile>(context, "tutorial.json"),
        leaderboard    = load<LeaderboardFile>(context, "leaderboard_bots.json"),
    )
}
```

## 3. Pemuat i18n

```kotlin
class I18n(context: Context, lang: String) {
    private val strings: Map<String, String> = run {
        val f = load<I18nFile>(context, "i18n/$lang.json")
        f.strings
    }
    operator fun get(key: String, vararg args: Pair<String, Any?>): String =
        args.fold(strings[key] ?: key) { acc, (k, v) -> acc.replace("{$k}", v?.toString() ?: "") }
}

// Contoh:
// i18n["co.co_app_t1_01.name"]                  -> "Piksel Global"
// i18n["notif.auction_won.body", "company" to nm] -> "Piksel Global kini milik anda..."
```

Pariti kunci **dijamin oleh validator** (setiap kunci en wujud dalam ms & id).
Nama khas (syarikat, bandar, orang) bernilai sama dalam ketiga-tiga bahasa.

## 4. Nota medan penting (setiap fail)

- **balance.json** — pemalar tunggal ekonomi. Baca sekali; jangan hardcode
  2%/95%/40%/8%/1.15/35%/48 jam dalam kod app; ambil dari sini.
- **tiers.json** — `baseValueA` = A dalam formula NT;
  `targetDailyNetIncome` = sasaran harian tier; `reputationThreshold`
  = ambang naik tier (null untuk t1).
- **sectors.json** — `multiplier` = M_sektor (musim dari seasons.json
  didarab masa jalan); `synergySectors` untuk bonus silang.
- **operations.json** — `unlockTier` = tier pembuka (satu jenis setiap tier);
  kos aras L = `baseCost * 1.15^(L-1)`; pendapatan aras L =
  `baseIncomePerHour * incomeGrowthPerLevel^(L-1)`; `maxLevel` = 10.
- **companies.json** — `ntValue`, `auctionStartPriceTM`, `paybackDays`
  telah DIKIRA dan DISAHKAN oleh validator. Untuk legacy:
  `auctionStartPriceTM` termasuk `premiumPct`; `formerOwnerCeoId` merujuk
  `ai_ceos.json`. Kategori mengikut tier: t1 starter, t2-t3 midmarket,
  t4-t5 rare, t6-t8 mega, legacy berasingan.
- **ai_ceos.json** — `aggression` 0-1, `maxPremiumOverNT` (nisbah),
  `entryDelayMinutes` kelewatan masuk lelongan, `auctionBoss` = pembangkit
  bidaan untuk sasaran legacy.
- **staff_roles.json** — `salaryByTier` (gaji/hari, terikat tier);
  kos ambil = `hireBaseCostPerStarTM * star * hireTierScale[tierIndex]`.
- **events.json** — enam kumpulan; kesan semua berangka; ganjaran hanya
  TM/DP/kosmetik kecil. `tierBand` (1-4) memetakan T1-2, T3-4, T5-6, T7-8.
- **seasons.json** — `seasonMultiplier` masuk ke M; trek premium TIDAK
  mengandungi TM/DP (hanya kosmetik/KM kecil/keselesaan).
- **tutorial.json** — `starterGrant.tm` diberi pada langkah pertama;
  `starterTarget` BERSKRIP: ciri lelongan T1 termurah, tanpa bidaan AI
  selama 8 minit (jangan guna logik lelongan biasa di sini).
- **leaderboard_bots.json** — 29 bot + `namePool` 120 nama untuk ganti
  bot yang "dipromosi"; skor mingguan = base ± variance.
- **i18n/*.json** — `strings` rata (kunci -> teks). Had panjang dijamin:
  nama/tajuk 28, butang 16, keterangan 140, berita 90.

## 5. Semakan integriti semasa runtime (disyorkan ringkas)

```kotlin
fun sanity(d: GameData): Boolean =
    d.companies.size == 216 &&
    d.companies.count { it.category == "legacy" } == 24 &&
    d.operations.size == 24 &&
    d.companies.all { it.auctionStartPriceTM > 0 && it.ntValue > 0 }
```

Versi penuh pemeriksaan ada dalam `tools/validate.py` (jalan semasa CI).
Jika `dataVersion` dalam aset != versi jangkaan app, dayakan migrasi/pindah muat.
