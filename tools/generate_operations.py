#!/usr/bin/env python3
"""Jana game-data/operations.json - 24 operasi (3 sektor x 8 jenis).

Pendapatan asas diselesaikan oleh tools/calibrate.py (seed tetap) supaya
pendapatan harian bersih setiap tier menghampiri sasaran dalam 15%.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calibrate import build_operations, verify  # noqa: E402
from common import GAME_DATA, data_version, save_json  # noqa: E402

ops = build_operations()
rep = verify(ops)
bad = [T for T, r in rep.items() if abs(r["dev_pct"]) > 15]
if bad:
    raise SystemExit(f"Kalibrasi gagal untuk tier: {bad} - baiki calibrate.py dahulu")

save_json(GAME_DATA / "operations.json", {"dataVersion": data_version(), "operations": ops})
print(f"operations.json dijana ({len(ops)} operasi); sisihan tier: "
      + ", ".join(f"T{t}:{r['dev_pct']:+.1f}%" for t, r in rep.items()))
