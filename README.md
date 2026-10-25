# Meridian Tycoon — Repo Data Game

Repo ini mengandungi **semua data dalaman** untuk game mudah alih *Meridian Tycoon*
(game tycoon: pemain ialah CEO yang naik 8 tier syarikat dengan membeli syarikat
melalui lelongan). Tiada kod APK di sini — hanya data siap-guna, skema, alat penjanaan,
validator dan dokumentasi integrasi.

## Struktur Repo

```
game-data/        Fail JSON akhir untuk app (salin terus ke app/src/main/assets/data/)
game-data/i18n/   en.json, ms.json, id.json (kunci teks pemain, pariti penuh 3 bahasa)
schema/           JSON Schema (draft-07) untuk setiap fail data
tools/            generate_*.py (penjana berangka berseed), validate.py, calibrate.py
reports/          data_report.md (dijana automatik oleh validator)
docs/             INTEGRATION.md, ECONOMY_NOTES.md, DECISIONS.md
Models.kt         Data class Kotlin (kotlinx.serialization) sepadan dengan skema
.github/workflows/  validate.yml (setiap push) & release.yml (tag v* -> Release)
```

## Senarai Fail Data (16 kumpulan)

| # | Fail | Kandungan |
|---|------|-----------|
| 1 | `balance.json` | Pemalar ekonomi teras (satu sumber kebenaran) |
| 2 | `tiers.json` | 8 tier syarikat (A, sasaran harian, ambang reputasi, ganjaran) |
| 3 | `sectors.json` | 3 sektor (app, fnb, logistics): pengganda M, sinergi, warna |
| 4 | `operations.json` | 24 operasi (3 sektor x 8 jenis, satu dibuka setiap tier) |
| 5 | `companies.json` | 216 syarikat (192 biasa + 24 legacy) dengan NT/harga/payback |
| 6 | `ai_ceos.json` | 7 profil CEO AI yang membida dalam lelongan |
| 7 | `staff_roles.json` | 5 peranan staf (COO, CFO, CMO, CTO, HR): kemahiran & gaji |
| 8 | `staff_pool.json` | 100 individu staf rekaan (5 peranan x 5 bintang x 4) |
| 9 | `research.json` | 12 node penyelidikan (3 pohon x 4 peringkat) |
| 10 | `events.json` | Habis Stok, Perang Bidaan, kontrak harian, sasaran mingguan, berita pasar, mikro-event |
| 11 | `seasons.json` | 6 musim x 6 minggu, trek ganjaran percuma + premium |
| 12 | `cosmetics.json` | 44 kosmetik (kulit logo, tema markas, gelaran CEO) — harga KM tetap |
| 13 | `milestones.json` | 30 milestone (6 teras + 24 tambahan, ganjaran DP) |
| 14 | `tutorial.json` | 10 langkah tutorial + starterGrant + sasaran starter berskrip |
| 15 | `leaderboard_bots.json` | 29 bot + kolam 120 nama untuk "pocket league" 30 pemain |
| 16 | `i18n/*.json` | Semua teks pemain (en, ms, id) termasuk 40 petua & templat laporan bidaan |

## Formula Ekonomi (WAJIB — lihat docs/ECONOMY_NOTES.md)

- `NT = A x (1 + 0.10 x P + 0.005 x R) x M` — nilai syarikat
  (A = asas nilai tier, P = pendapatan sejam dalam ribuan TM, R = reputasi 0-100,
  M = pengganda sektor x musim)
- Harga mula lelongan = `0.95 x NT`
- Payback (hari) = `harga mula / (0.35 x P x 1000 x 24)`

## Cara Jana Semula & Validasi

```bash
pip install jsonschema
python tools/generate_balance.py          # (setiap generate_*.py dengan seed tetap)
python tools/validate.py --report         # validator penuh + jana reports/data_report.md
python tools/validate.py --strict         # mod ketat CI release (semua 16 fail wajib)
```

Semua bahagian berangka dijana oleh skrip Python dengan **seed tetap** supaya boleh
diulang 100%. Bahagian teks (nama, sejarah, berita) ialah rekaan asli dan disimpan
sebagai **kunci i18n** — fail data tidak mengandungi teks pemain.

## Integrasi Ke Android

Salin kandungan `game-data/` ke `app/src/main/assets/data/`. Contoh penuh dengan
kotlinx.serialization ada dalam `docs/INTEGRATION.md`; data class sedia-guna ada
dalam `Models.kt`.

## CI & Release

- `validate.yml` — validasi penuh pada setiap push / PR.
- `release.yml` — pada tag `v*`: validasi ketat, bina `meridian-data-vX.Y.Z.zip`
  dan terbitkan ke GitHub Releases.

## Konvensyen Penting

- ID: `snake_case` dengan awalan jenis (`co_`, `ceo_`, `st_`, `rs_`, `ev_`, `sn_`, `cs_`, `ms_`, `op_`).
- Mata wang: **TM** (tunai), **DP** (dana pelabur), **KM** (kredit premium — kosmetik & keselesaan sahaja). Semua nilai integer.
- Had teks: nama syarikat 28 aksara, tajuk/gelaran 28, butang 16, keterangan 140, berita 90.
- Setiap fail data mengandungi medan `dataVersion` (semver).

Semua nama syarikat, CEO, staf, bandar dan jenama dalam repo ini adalah **rekaan sepenuhnya**.
