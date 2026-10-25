#!/usr/bin/env python3
"""Jana game-data/leaderboard_bots.json - 29 bot + kolam 120 nama rekaan
untuk "pocket league" 30 pemain (pemain + 29 bot).

weeklyScoreBase mengikut tier = 7 x sasaran harian tier x faktor 0.70-1.15
(deterministik); varians 15-30% daripada asas.
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text_names as TN  # noqa: E402
from common import GAME_DATA, SEED, TIERS, data_version, save_json  # noqa: E402

rng = random.Random(SEED + 500)

TIER_DIST = [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5,
             6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8]
STYLES = ["steady", "aggressive", "sniper", "diversifier"]

bots = []
name_map = {}
for i, tier in enumerate(TIER_DIST, start=1):
    target = TIERS[tier - 1][2]
    factor = 0.70 + ((SEED + i * 31) % 46) / 100.0  # 0.70-1.15 stabil
    base = int(target * 7 * factor // 100 * 100)
    var = int(base * rng.uniform(0.15, 0.30) // 100 * 100)
    bid = f"lb_bot_{i:02d}"
    nkey = f"lb.bot.{i:02d}.name"
    name_map[nkey] = TN.person_name(TN.BOT_OFFSET, i - 1)
    bots.append({
        "id": bid,
        "nameKey": nkey,
        "tier": tier,
        "weeklyScoreBase": base,
        "weeklyScoreVariance": var,
        "style": STYLES[(SEED + i * 13) % 4],
    })

pool = []
for j in range(1, 121):
    key = f"lb.pool.{j:03d}"
    name_map[key] = TN.person_name(TN.BOTPOOL_OFFSET, j - 1)
    pool.append({"index": j, "nameKey": key})

if __name__ == "__main__":
    save_json(GAME_DATA / "leaderboard_bots.json",
              {"dataVersion": data_version(), "leagueSize": 30, "bots": bots, "namePool": pool})
    (GAME_DATA.parent / "tools" / "generated").mkdir(exist_ok=True)
    (GAME_DATA.parent / "tools" / "generated" / "bot_names.json").write_text(
        json.dumps(name_map, ensure_ascii=False, indent=2), encoding="utf-8")
    vals = list(name_map.values())
    print(f"leaderboard_bots.json dijana (29 bot + 120 nama; unik: {len(set(vals)) == len(vals)})")
