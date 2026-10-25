#!/usr/bin/env python3
"""Jana game-data/tiers.json - 8 tier syarikat."""
from common import GAME_DATA, TIERS, data_version, save_json

MAX_OPERATIONS = [3, 6, 9, 12, 15, 18, 21, 24]
MAX_STAFF = [6, 8, 10, 12, 14, 16, 18, 20]

tiers = []
for i, (tid, a, target, rep, dp) in enumerate(TIERS, start=1):
    tiers.append({
        "id": tid,
        "titleKey": f"tier.{tid}.title",
        "maxOperations": MAX_OPERATIONS[i - 1],
        "maxStaff": MAX_STAFF[i - 1],
        "baseValueA": a,
        "targetDailyNetIncome": target,
        "reputationThreshold": rep,
        "tierUpRewardDP": dp,
        "rewardKey": f"tier.{tid}.reward" if dp is not None else None,
    })

if __name__ == "__main__":
    save_json(GAME_DATA / "tiers.json", {"dataVersion": data_version(), "tiers": tiers})
    print("tiers.json dijana")
