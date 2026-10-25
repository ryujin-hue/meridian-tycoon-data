#!/usr/bin/env python3
"""Jana game-data/research.json - 12 node: 3 pohon x 4 peringkat.

Peraturan: kesan tetap atau berperingkat DENGAN had keras (tiada pengganda
tanpa had); tiada node yang mengunci kandungan teras. Semua kos dalam DP.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, data_version, save_json  # noqa: E402

# (id, tree, stage, nameKey-false, costDP, unlockTier, effect)
RESEARCH = [
    # Pohon Operasi - kelancaran harian
    ("rs_op_1", "operasi", 1, 20, 1, {"type": "operations_income_pct", "perStageValue": 3, "hardCapValue": 12}),
    ("rs_op_2", "operasi", 2, 30, 2, {"type": "offline_cap_hours", "perStageValue": 1, "hardCapValue": 12}),
    ("rs_op_3", "operasi", 3, 45, 4, {"type": "upgrade_cost_reduction_pct", "perStageValue": 2, "hardCapValue": 8}),
    ("rs_op_4", "operasi", 4, 80, 6, {"type": "operations_income_pct", "perStageValue": 5, "hardCapValue": 5}),
    # Pohon Pasaran - reputasi & kontrak
    ("rs_mk_1", "pasaran", 1, 20, 2, {"type": "reputation_gain_pct", "perStageValue": 5, "hardCapValue": 20}),
    ("rs_mk_2", "pasaran", 2, 35, 3, {"type": "contract_reward_pct", "perStageValue": 5, "hardCapValue": 15}),
    ("rs_mk_3", "pasaran", 3, 50, 5, {"type": "market_news_boost_pct", "perStageValue": 2, "hardCapValue": 8}),
    ("rs_mk_4", "pasaran", 4, 70, 7, {"type": "market_scan_duration_hours", "perStageValue": 6, "hardCapValue": 6}),
    # Pohon Merger - lelongan & legacy
    ("rs_mg_1", "merger", 1, 25, 3, {"type": "auction_fee_reduction_pct", "perStageValue": 0.2, "hardCapValue": 0.8}),
    ("rs_mg_2", "merger", 2, 40, 4, {"type": "bid_insight_pct", "perStageValue": 1, "hardCapValue": 3}),
    ("rs_mg_3", "merger", 3, 60, 6, {"type": "respawn_reduction_hours", "perStageValue": 6, "hardCapValue": 18}),
    ("rs_mg_4", "merger", 4, 100, 8, {"type": "legacy_premium_reduction_pct", "perStageValue": 2, "hardCapValue": 2}),
]

nodes = []
for rid, tree, stage, dp, tier, eff in RESEARCH:
    nodes.append({
        "id": rid,
        "tree": tree,
        "stage": stage,
        "nameKey": f"rs.{rid}.name",
        "descKey": f"rs.{rid}.desc",
        "costDP": dp,
        "unlockTier": tier,
        "effect": eff,
    })

if __name__ == "__main__":
    save_json(GAME_DATA / "research.json", {"dataVersion": data_version(), "nodes": nodes})
    print("research.json dijana (12 node; semua kesan ada had keras)")
