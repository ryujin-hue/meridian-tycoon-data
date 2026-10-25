#!/usr/bin/env python3
"""Jana game-data/seasons.json - 6 musim x 6 minggu.

Trek percuma: TM/DP/KM kecil/kosmetik.
Trek premium: kosmetik, KM kecil & keselesaan sahaja (auto-kutip sekali
sehari, wishlist pasar) - TIADA TM/DP, kuasa ekonomi, kelebihan bidaan
atau loot box.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, SEED, data_version, save_json  # noqa: E402

rng = random.Random(SEED + 400)

MULTS = [0.95, 1.00, 1.05, 1.10, 1.20, 1.25]
FREE_COSMETICS = ["cs_logo_05", "cs_logo_06", "cs_logo_07", "cs_hq_05",
                  "cs_hq_06", "cs_logo_08", "cs_logo_09", "cs_hq_07",
                  "cs_logo_10", "cs_logo_11", "cs_hq_08", "cs_logo_12"]
PREM_COSMETICS = ["cs_title_17", "cs_title_18", "cs_title_19", "cs_title_20",
                  "cs_title_21", "cs_title_22", "cs_title_23", "cs_title_24",
                  "cs_hq_03", "cs_hq_04", "cs_logo_03", "cs_logo_04"]


def free_track(season: int, cos_ref: str) -> dict:
    base_tm = int(1200 * (2.2 ** (season - 1)))
    steps = []
    for s in range(1, 21):
        rewards = []
        if s in (4, 8, 12, 16, 19):
            rewards.append({"type": "dp", "amount": 2 + season + s // 4})
        elif s in (6, 13, 18):
            rewards.append({"type": "km", "amount": 5 + season})
        elif s == 10:
            rewards.append({"type": "cosmetic", "ref": cos_ref})
        elif s == 20:
            rewards.append({"type": "cosmetic", "ref": cos_ref})
            rewards.append({"type": "dp", "amount": 5 + season * 2})
        else:
            tm = int(base_tm * rng.uniform(0.85, 1.3) // 100 * 100)
            rewards.append({"type": "tm", "amount": max(200, tm)})
        steps.append({"step": s, "rewards": rewards})
    return {"steps": steps}


def premium_track(season: int, cos_a: str, cos_b: str) -> dict:
    steps = []
    for s in range(1, 21):
        rewards = []
        if s == 7:
            rewards.append({"type": "comfort", "ref": "auto_collect_daily"})
        elif s == 14:
            rewards.append({"type": "comfort", "ref": "market_wishlist"})
        elif s in (5, 10, 15, 20):
            rewards.append({"type": "cosmetic", "ref": cos_a if s % 10 == 0 else cos_b})
        else:
            rewards.append({"type": "km", "amount": 3 + s // 3})
        steps.append({"step": s, "rewards": rewards})
    return {"steps": steps}


seasons = []
for i in range(1, 7):
    seasons.append({
        "id": f"sn_{i}",
        "nameKey": f"sn.sn_{i}.name",
        "descKey": f"sn.sn_{i}.desc",
        "weeksPerSeason": 6,
        "seasonMultiplier": MULTS[i - 1],
        "freeTrack": free_track(i, FREE_COSMETICS[i - 1]),
        "premiumTrack": premium_track(i, PREM_COSMETICS[(i - 1) * 2],
                                      PREM_COSMETICS[(i - 1) * 2 + 1]),
    })

if __name__ == "__main__":
    save_json(GAME_DATA / "seasons.json", {"dataVersion": data_version(), "seasons": seasons})
    print("seasons.json dijana (6 musim x 6 minggu; premium tanpa kuasa ekonomi)")
