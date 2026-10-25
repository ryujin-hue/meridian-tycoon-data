# ECONOMY_NOTES.md — Nota Ekonomi Meridian Tycoon

Dokumen ini merakamkan **semua keputusan berangka**, hasil kalibrasi dan
penyimpangan yang dijangka. Formula di sini adalah **satu-satunya kebenaran**;
validator (tools/validate.py) mengira semula setiap nilai.

## 1. Formula Teras (GDD — tidak diubah)

```
NT           = A x (1 + 0.10 x P + 0.005 x R) x M
Harga mula   = 0.95 x NT                    (legacy: x (1 + premiumPct/100))
Payback (hari) = harga mula / (0.35 x P x 1000 x 24)
P daripada D : P = 0.95.A.M.(1+0.005R) / (D.8400 - 0.095.A.M)
```

- `P` = pendapatan kasar sejam dalam **ribu** TM; `R` = reputasi 0-100;
  `A` = asas nilai tier; `M` = pengganda sektor x musim.
- Dalam data statik, `M = M_sektor` sahaja (app 1.15, logistics 1.00, fnb 0.90);
  pengganda musim (0.95-1.25) didarab semasa runtime.
- 0.35 = sumbangan bersih syarikat dibeli (balance.json).
- 8400 = 0.35 x 1000 x 24 (penukaran P-ribu ke pendapatan harian bersih).

### Tiga contoh rujukan (validator mengesahkan secara eksak)

| A | P | R | M | NT |
|---|---|---|---|-----|
| 150,000 | 2.4 | 35 | 1.10 | **233,475** |
| 400,000 | 5.2 | 62 | 0.95 | **695,400** |
| 3,000,000 | 14.0 | 78 | 1.25 | **10,462,500** |

## 2. Sasaran Payback — Keputusan Sebenar

| Tier | Band sasaran | Payback terhasil (min-median-maks) |
|------|--------------|-------------------------------------|
| T1   | (pilihan kami: 15-25 hari, lihat DECISIONS.md) | 15.2 - 19.2 - 25.1 |
| T2-T4| 10-20 hari | 10.6 - ~15 - 19.3 (semua dalam band) |
| T5   | 20-40 hari | 31.8 - 35.1 - 38.9 (adaptif untuk kekal NT <= 3M) |
| T6-T8| dilaporkan sahaja | T6 62-92; T7 149-220; T8 333-453 hari |

## 3. Penyimpangan NT Yang Dijangka (formula menang, dilaporkan)

Panduan mega 3M-24M **tidak dapat dipenuhi sepenuhnya** pada T7-T8:

1. **Had bawah matematik payback** — dengan P → besar,
   `payback → 0.95 x 0.1 x A x M / 8400 = A x M / 88,421`.
   Maka T6 >= ~34-39 hari, T7 >= ~96-110 hari, T8 >= ~271-312 hari,
   TIDAK KIRA bagaimana P dipilih. Ini sifat formula dengan A yang besar.
2. **T8 NT** — walaupun P kecil (1 ribu TM/jam), NT = 24M x (1.1+0.005R) x M
   >= ~24M. Tetapi P sekecil itu menjadikan syarikat mega tidak bermakna
   sebagai sumber pendapatan (3-4% sasaran harian). Kami memilih P 30-45
   supaya sumbangan bersih syarikat T8 = 12-18% sasaran harian tier —
   akibatnya NT T8 = 101.5M-161.3M (melebihi panduan 24M). **Perdagangan
   yang sedar:** nilai harga vs fungsi pendapatan; formula dipertahankan.
3. **T7 NT** — P 14-24 + R 60-80 memberi NT 23.1M-27.3M (sebahagian kecil
   di atas panduan). Payback 149-220 hari adalah perangkap matematik #1.
4. **T1 NT** boleh berada bawah A (contoh 38.5k < 40k) kerana pengganda
   sektor fnb 0.90 — normal dan dijangka (tiada panduan NT untuk starter).

Semua penyimpangan ini dikeluarkan sebagai AMARAN oleh validator dan
dilaporkan dalam reports/data_report.md.

## 4. Kalibrasi Operasi (tools/calibrate.py)

Model pemain aktif:
- 16 jam kutipan sehari; gaji harian = 20% pendapatan kasar
  → pendapatan bersih operasi = 0.80 x 16 x jumlah pendapatan sejam.
- Aras rujukan operasi pada tier T: `L(k,T) = min(10, T-k+2)`
  (operasi jenis k dibuka pada tier k; pemain menaik taraf ~1 aras per tier).
- `baseIncomePerHour(sektor, jenis k) = b_k x M_sektor`; `b_k` diselesaikan
  secara greedy supaya setiap tier mencapai **100% sasaran harian**
  (keputusan tafsiran — lihat DECISIONS.md #3), toleransi validator 15%.

Keputusan (sisihan vs sasaran): **semua tier <= 0.05%** (praktikal 0%).

| Tier | Sasaran harian (TM) | Pendapatan bersih operasi terhasil |
|------|---------------------|-------------------------------------|
| T1 | 6,000 | 6,000 (±0%) |
| T2 | 14,000 | 14,000 (±0%) |
| T3 | 32,000 | 32,000 (±0%) |
| T4 | 75,000 | 75,000 (±0%) |
| T5 | 170,000 | 170,000 (±0%) |
| T6 | 400,000 | 400,000 (±0%) |
| T7 | 950,000 | 950,000 (±0%) |
| T8 | 2,200,000 | 2,200,000 (±0%) |

Kos operasi: `baseCost = 150 x baseIncomePerHour` (dibundar 10) — payback
operasi pertama ~11.7 hari bersih; `costGrowth 1.15` seperti GDD.

## 5. Gaji & Staf

Gaji terikat **tier** (bukan baki tunai). Baseline = 20% x pendapatan kasar
operasi ÷ bilangan staf tipikal (T+3 orang): 560/1,050/2,000/4,000/8,000/
16,700/35,500/75,000 TM per hari untuk T1-T8; didarab peranan
(COO/CFO x1.15, CMO x1.05, CTO x1.20, HR x0.90). Kos ambil =
`2500 x star x hireTierScale[tier]`.

## 6. Lain-lain

- **Premium legacy 15-25%** dikenakan pada harga mula (0.95 x NT x premium);
  payback legacy dikira daripada harga termasuk premium (lebih panjang —
  disengajakan: legacy = prestij).
- **Pembundaran**: P dibundar 2 titik perpuluhan; NT & harga mula integer;
  payback 2 titik perpuluhan. Validator mengira semula daripada nilai
  tersimpan dan menuntut kepadanan eksak (toleransi payback 0.02 hari).
- **Julat NT tercapai**: midmarket 84k-255k (panduan 80k-400k ✓);
  rare 629k-2.99M (400k-3M ✓); mega T6 6.3M-10.8M ✓, T7/T8 di luar (§3).
- **Sasaran kalah 48 jam** dan **simpanan offline 8 jam** adalah pemalar
  runtime; penyelidikan boleh mengurangkan/ menambah dengan HAD KERAS
  (offline maks 12j; respawn minima 30j; yuran lelongan minima 1.2%).
