# DECISIONS.md — Keputusan Reka Bentuk & Tafsiran

Setiap keputusan yang membuat tafsiran terhadap spesifikasi direkodkan di
sini supaya boleh disemak dan diubah dengan sedar.

1. **Pembungkus fail tatasusunan** — Spesifikasi menuntut medan `dataVersion`
   pada SETIAP fail. Fail berbentuk senarai dibungkus objek
   `{ "dataVersion": "...", "<field>": [...] }`. Models.kt dan skema
   mengikut bentuk ini.

2. **Seed tetap** — `SEED = 20261025` dalam tools/common.py; setiap penjana
   menggunakan ofset tetap (+100 syarikat, +300 events, +400 musim, +500 bot,
   +700 pertumbuhan operasi). Penjanaan 100% boleh diulang.

3. **Tafsiran liputan operasi vs sasaran** — GDD: "syarikat dibeli menyumbang
   paling banyak 30%" (andainya untuk kalibrasi). DoD pula menuntut
   "pendapatan harian OPERASI dalam toleransi 15% bagi setiap tier". Kami
   memilih: **operasi sahaja dikalibrasi ke 100% sasaran** (julat selamat
   85-115%), syarikat dibeli menambah di atasnya (pemain yang memiliki
   syarikat pendapatan tinggi akan melebihi sasaran — sasaran bertindak
   sebagai lantai). Andainya 30% direkodkan dalam balance.json untuk rujukan
   pereka. Perhatikan: syarikat T1 terhasil menyumbang ~35-50% sasaran T1
   secara individu pada hujung pendek payback — ketegangan yang diakui,
   tidak membahayakan (lihat ECONOMY_NOTES.md §4).

4. **Payback T1 = 15-25 hari** — Spesifikasi tidak menetapkan band untuk T1
   (starter). 15-25 hari memberi sumbangan munasabah tanpa memunculkan
   ekonomi awal; starterGrant 50,000 TM menampung lelongan pertama.

5. **T6-T8: P dipilih untuk fungsi pendapatan** — NT/payback T6-T8 hanya
   dilaporkan (per spesifikasi). P dipilih supaya syarikat mega kekal
   bermakna sebagai penjana pendapatan (12-18% sasaran harian T8). Akibat
   NT > panduan 24M pada T7/T8 — dijangka & dilaporkan (ECONOMY_NOTES.md §3).

6. **Legacy = 8 setiap sektor, asas tier 6/7/8 (3/3/2)** — memberi taburan
   prestij; premium 15-25% pada harga mula; `formerOwnerCeoId` merujuk CEO
   AI (ceo_victor_nyx, boss, memiliki legacy pertama setiap sektor).

7. **Nama khas sama dalam 3 bahasa** — Nama syarikat/orang/bandar ialah
   proper noun; nilainya sama dalam en/ms/id (kunci tetap wujud di semua
   fail). Penerangan/sejarah/bio diterjemah penuh. Senarai sekatan jenama
   sebenar disemak oleh validator (padanan perkataan penuh).

8. **`statKey` bukan kunci i18n** — medan `statKey` (staff_roles) ialah
   pengenal teknikal, bukan rujukan teks; tidak disemak terhadap i18n.

9. **M statik = sektor sahaja** — pengganda musim (0.95-1.25) daripada
   seasons.json didarab semasa runtime; NT tersimpan menggunakan M sektor
   supaya harga kekal deterministik merentas musim.

10. **Sasaran starter berskrip** — ditanda `special: true` dan dikecualikan
    daripada formula normal: lelongan termurah T1 (maks 45,000 TM mula)
    dipaparkan tanpa bidaan AI selama 8 minit; starterGrant 50,000 TM
    menjamin pembelian pertama dalam 8 minit. Tidak mengubah sebarang
    pemalar ekonomi.

11. **Trek premium musim** — diintepretasi ketat: TIADA TM/DP pada trek
    premium (hanya kosmetik, KM kecil 3-10/step, dan 2 item keselesaan).
    Kuasa ekonomi/kelebihan bidaan/loot box tiada di mana-mana trek.

12. **Gaji staf** — baseline daripada andainya kalibrasi (20% kasar, T+3
    staf), didarab peranan; disimpan sebagai jadual 8 tier dalam
    staff_roles.json supaya app tidak perlu mengira.

13. **dataVersion 0.9.0 semasa pembangunan → 1.0.0 pada tag v1.0.0.**
