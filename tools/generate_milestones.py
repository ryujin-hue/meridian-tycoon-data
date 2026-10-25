#!/usr/bin/env python3
"""Jana game-data/milestones.json - 30 milestone:
6 teras GDD (pembelian pertama, dua sektor, reputasi 60, penguasaan sektor,
empayar dwitier, Naik Tier 8) + 24 tambahan dengan ganjaran DP.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, data_version, save_json  # noqa: E402

CORE = [
    ("ms_first_purchase", "companies_owned", 1, None, 10, "cs_title_01"),
    ("ms_two_sectors", "sectors_active", 2, None, 15, None),
    ("ms_rep_60", "reputation", 60, None, 25, None),
    ("ms_sector_mastery", "sector_mastery", 1, "app", 30, "cs_title_04"),
    ("ms_dual_tier_empire", "dual_tier_empire", 1, None, 40, None),
    ("ms_tier_8", "tier_reached", 8, None, 100, "cs_title_08"),
]

EXTRA = [
    ("ms_auctions_5", "auctions_won", 5, 10, None),
    ("ms_auctions_15", "auctions_won", 15, 20, None),
    ("ms_auctions_40", "auctions_won", 40, 35, None),
    ("ms_companies_5", "companies_owned", 5, 10, None),
    ("ms_companies_15", "companies_owned", 15, 15, None),
    ("ms_companies_30", "companies_owned", 30, 25, None),
    ("ms_companies_50", "companies_owned", 50, 40, None),
    ("ms_upgrades_25", "operations_upgraded", 25, 10, None),
    ("ms_upgrades_100", "operations_upgraded", 100, 20, None),
    ("ms_upgrades_300", "operations_upgraded", 300, 35, None),
    ("ms_staff_5", "staff_hired", 5, 8, None),
    ("ms_staff_15", "staff_hired", 15, 15, None),
    ("ms_research_4", "research_completed", 4, 10, None),
    ("ms_research_8", "research_completed", 8, 20, None),
    ("ms_research_12", "research_completed", 12, 30, None),
    ("ms_contracts_10", "contracts_completed", 10, 10, None),
    ("ms_contracts_40", "contracts_completed", 40, 20, None),
    ("ms_contracts_100", "contracts_completed", 100, 35, None),
    ("ms_seasons_1", "seasons_played", 1, 10, None),
    ("ms_seasons_3", "seasons_played", 3, 20, None),
    ("ms_cosmetics_3", "cosmetics_owned", 3, 8, None),
    ("ms_cosmetics_10", "cosmetics_owned", 10, 15, None),
    ("ms_rep_30", "reputation", 30, 8, None),
    ("ms_rep_90", "reputation", 90, 25, None),
]

milestones = []
for mid, gtype, val, sector, dp, cos in CORE:
    milestones.append({
        "id": mid, "core": True,
        "nameKey": f"ms.{mid}.name",
        "descKey": f"ms.{mid}.desc",
        "goal": {"type": gtype, "value": val, "sector": sector},
        "reward": {"dp": dp, "cosmeticRef": cos},
    })
for mid, gtype, val, dp, _ in EXTRA:
    milestones.append({
        "id": mid, "core": False,
        "nameKey": f"ms.{mid}.name",
        "descKey": f"ms.{mid}.desc",
        "goal": {"type": gtype, "value": val, "sector": None},
        "reward": {"dp": dp, "cosmeticRef": None},
    })

if __name__ == "__main__":
    save_json(GAME_DATA / "milestones.json", {"dataVersion": data_version(), "milestones": milestones})
    print(f"milestones.json dijana ({len(milestones)} = 6 teras + {len(EXTRA)} tambahan)")
