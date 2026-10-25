#!/usr/bin/env python3
"""Kalibrasi pendapatan operasi supaya pendapatan harian bersih pemain aktif
menghampiri sasaran harian setiap tier dalam toleransi 15%.

Model rujukan (lihat docs/DECISIONS.md):
- Pemain aktif mengutip 16 jam sehari; gaji harian = 20% pendapatan kasar
  -> pendapatan bersih operasi = 0.80 x 16 jam x jumlah pendapatan sejam.
- Operasi jenis k sektor s dibuka pada tier k; pada tier T pemain memiliki
  operasi k = 1..T pada aras rujukan L(k,T) = min(10, T-k+2).
- baseIncomePerHour(sektor s, jenis k) = b_k x M_s  (M_s = pengganda sektor).
- calibrate.py menyelesaikan b_k secara greedy per tier supaya jumlah
  pendapatan sejam mencapai sasaran tier.

Jalankan: python tools/calibrate.py [--verify]  (mod --verify baca operations.json)
"""
import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

G_MIN, G_MAX = 1.08, 1.14
MAX_LEVEL = 10


def ref_level(k: int, T: int) -> int:
    """Aras rujukan operasi jenis k semasa pemain berada di tier T."""
    return min(MAX_LEVEL, T - k + 2)


def assign_growth(seed_offset: int = 0) -> dict:
    """incomeGrowthPerLevel untuk setiap (sektor, jenis) - seed tetap."""
    rng = random.Random(C.SEED + 700 + seed_offset)
    return {
        (s, k): round(rng.uniform(G_MIN, G_MAX), 3)
        for s in C.SECTORS for k in range(1, 9)
    }


def solve_base_incomes(growth: dict) -> dict:
    """Selesaikan b_k -> kembalikan {(sektor, jenis): baseIncomePerHour}."""
    base = {}
    for T in range(1, 9):
        target = C.TIERS[T - 1][2]
        need_hourly = target / ((1 - C.SALARY_SHARE) * C.ACTIVE_H)
        have = 0.0
        for s in C.SECTORS:
            for k in range(1, T):
                have += base[(s, k)] * growth[(s, k)] ** (ref_level(k, T) - 1)
        new_factor = sum(
            C.SECTOR_MULT[s] * growth[(s, T)] ** (ref_level(T, T) - 1)
            for s in C.SECTORS
        )
        b_T = (need_hourly - have) / new_factor
        for s in C.SECTORS:
            base[(s, T)] = round(b_T * C.SECTOR_MULT[s], 2)
    return base


def build_operations() -> list:
    growth = assign_growth()
    base = solve_base_incomes(growth)
    ops = []
    for s in C.SECTORS:
        for k in range(1, 9):
            inc = base[(s, k)]
            ops.append({
                "id": f"op_{s}_{k}",
                "sector": s,
                "unlockTier": k,
                "nameKey": f"op.{s}.{k}.name",
                "descKey": f"op.{s}.{k}.desc",
                "baseCost": int(round(150 * inc / 10.0) * 10),
                "costGrowth": C.UPGRADE_COST_GROWTH,
                "baseIncomePerHour": inc,
                "incomeGrowthPerLevel": growth[(s, k)],
                "maxLevel": MAX_LEVEL,
            })
    return ops


def verify(ops: list) -> dict:
    """Pendapatan harian bersih mengikut tier + penyimpangan % vs sasaran."""
    by_key = {(o["sector"], int(o["id"].split("_")[-1])): o for o in ops}
    out = {}
    for T in range(1, 9):
        total = 0.0
        for s in C.SECTORS:
            for k in range(1, T + 1):
                o = by_key[(s, k)]
                total += o["baseIncomePerHour"] * o["incomeGrowthPerLevel"] ** (ref_level(k, T) - 1)
        daily_net = (1 - C.SALARY_SHARE) * C.ACTIVE_H * total
        target = C.TIERS[T - 1][2]
        out[T] = {"daily_net": round(daily_net), "target": target,
                  "dev_pct": round((daily_net - target) / target * 100, 2)}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="baca operations.json dan laporkan")
    args = ap.parse_args()
    if args.verify:
        ops = C.load_json(C.GAME_DATA / "operations.json")
    else:
        ops = build_operations()
    rep = verify(ops)
    print(f"{'tier':<6}{'harian bersih':>16}{'sasaran':>12}{'sisihan':>10}")
    ok = True
    for T, r in rep.items():
        flag = "" if abs(r["dev_pct"]) <= 15 else "  <-- MELEBIHI 15%"
        ok &= abs(r["dev_pct"]) <= 15
        print(f"T{T:<5}{r['daily_net']:>16,}{r['target']:>12,}{r['dev_pct']:>+9.2f}%{flag}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
