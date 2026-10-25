# Laporan Data Meridian Tycoon

Dijana oleh tools/validate.py (dataVersion 0.9.0).

## Bilangan Entiti

| Fail | Bilangan | Sasaran |
|---|---|---|
| tiers | - | 8 |
| sectors | 3 | 3 |
| operations | - | 24 |
| companies | - | 216 |
| ai_ceos | 7 | 7 |
| staff_roles | - | 5 |
| staff_pool | - | 100 |
| research | - | 12 |
| seasons | - | 6 |
| cosmetics | - | 44 |
| milestones | - | 30 |
| tutorial | - | 10 |
| leaderboard_bots | - bot + 120 nama | 29 + 120 |

## Taburan NT & Payback mengikut Tier (syarikat bukan legacy)

| Tier | NT min | NT median | NT maks | Payback min | Payback median | Payback maks |
|---|---|---|---|---|---|---|
| t1 | 38,484 | 45,080 | 53,360 | 15.2 | 19.2 | 25.1 |
| t2 | 84,096 | 98,800 | 115,000 | 13.2 | 15.2 | 18.7 |
| t3 | 169,425 | 196,950 | 254,782 | 10.6 | 17.7 | 19.3 |
| t4 | 629,640 | 767,200 | 881,360 | 12.6 | 14.6 | 18.3 |
| t5 | 1,828,530 | 2,273,700 | 2,992,990 | 31.8 | 35.1 | 38.9 |
| t6 | 6,307,200 | 8,290,350 | 10,843,350 | 62.3 | 68.6 | 91.9 |
| t7 | 23,064,750 | 23,868,000 | 27,272,250 | 149.3 | 188.8 | 220.3 |
| t8 | 101,541,600 | 127,320,000 | 161,349,600 | 332.7 | 363.2 | 452.9 |

## Penyimpangan Pendapatan Harian Operasi vs Sasaran Tier

| Tier | Penyimpangan |
|---|---|
| t1 | +0.00% |
| t2 | +0.00% |
| t3 | +0.00% |
| t4 | +0.00% |
| t5 | -0.00% |
| t6 | -0.00% |
| t7 | -0.00% |
| t8 | -0.00% |

## Amaran

- staff_roles.json: tiada (dijana kemudian)
- staff_pool.json: tiada (dijana kemudian)
- research.json: tiada (dijana kemudian)
- events.json: tiada (dijana kemudian)
- seasons.json: tiada (dijana kemudian)
- cosmetics.json: tiada (dijana kemudian)
- milestones.json: tiada (dijana kemudian)
- tutorial.json: tiada (dijana kemudian)
- leaderboard_bots.json: tiada (dijana kemudian)
- companies: NT maks tier 7 (27,272,250) melebihi panduan mega 24,000,000 (formula diutamakan)
- companies: NT maks tier 8 (161,349,600) melebihi panduan mega 24,000,000 (formula diutamakan)
- companies: T8 NT minimum 101,541,600 > panduan mega 24,000,000 - secara matematik tidak dapat dielakkan (A=24,000,000); lihat docs/ECONOMY_NOTES.md
- i18n: tiada fail lagi
