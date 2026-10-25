#!/usr/bin/env python3
"""Jana game-data/staff_roles.json - 5 peranan: COO, CFO, CMO, CTO, HR.

Kemahiran aktif ikut GDD:
- Overtime (COO): operasi siap 30 minit lebih awal, setiap 6 jam
- Audit Clean (CFO): 50% faedah leverage dipulangkan
- Campaign (CMO): reputasi +6 dalam 48 jam, seminggu sekali
- Market Scan (CTO): NT tepat 24 jam
- Recruitment (HR): staf bintang 4 pada harga bintang 3, sebulan sekali

Gaji terikat TIER (bukan baki tunai): baseline daripada andaian kalibrasi
(gaji ~20% pendapatan kasar, bilangan staf tipikal T+3), didarab peranan.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, data_version, round_sig, save_json  # noqa: E402

BASE_SALARY = [560, 1050, 2000, 4000, 8000, 16700, 35500, 75000]
ROLE_MULT = {"coo": 1.15, "cfo": 1.15, "cmo": 1.05, "cto": 1.20, "hr": 0.90}


def salary(mult: float) -> list:
    return [int(round(v * mult / 10.0) * 10) for v in BASE_SALARY]


ROLES = [
    {
        "id": "coo",
        "passive": {"statKey": "operations_income", "perStarPct": 2.0, "hardCapPct": 10.0,
                    "descKey": "role.coo.passive"},
        "activeSkill": {"skillId": "overtime", "nameKey": "role.coo.active_name",
                        "descKey": "role.coo.active_desc",
                        "cooldownHours": 6, "unlockStar": 1},
    },
    {
        "id": "cfo",
        "passive": {"statKey": "leverage_interest_reduction", "perStarPct": 0.5, "hardCapPct": 2.5,
                    "descKey": "role.cfo.passive"},
        "activeSkill": {"skillId": "audit_clean", "nameKey": "role.cfo.active_name",
                        "descKey": "role.cfo.active_desc",
                        "cooldownHours": 72, "unlockStar": 2},
    },
    {
        "id": "cmo",
        "passive": {"statKey": "reputation_gain", "perStarPct": 5.0, "hardCapPct": 25.0,
                    "descKey": "role.cmo.passive"},
        "activeSkill": {"skillId": "campaign", "nameKey": "role.cmo.active_name",
                        "descKey": "role.cmo.active_desc",
                        "cooldownHours": 168, "unlockStar": 2},
    },
    {
        "id": "cto",
        "passive": {"statKey": "upgrade_cost_reduction", "perStarPct": 1.5, "hardCapPct": 7.5,
                    "descKey": "role.cto.passive"},
        "activeSkill": {"skillId": "market_scan", "nameKey": "role.cto.active_name",
                        "descKey": "role.cto.active_desc",
                        "cooldownHours": 48, "unlockStar": 3},
    },
    {
        "id": "hr",
        "passive": {"statKey": "hire_cost_reduction", "perStarPct": 4.0, "hardCapPct": 20.0,
                    "descKey": "role.hr.passive"},
        "activeSkill": {"skillId": "recruitment", "nameKey": "role.hr.active_name",
                        "descKey": "role.hr.active_desc",
                        "cooldownHours": 720, "unlockStar": 3},
    },
]

roles = []
for r in ROLES:
    roles.append({
        "id": r["id"],
        "nameKey": f"role.{r['id']}.name",
        "descKey": f"role.{r['id']}.desc",
        "passive": r["passive"],
        "activeSkill": r["activeSkill"],
        "salaryByTier": salary(ROLE_MULT[r["id"]]),
        "hireBaseCostPerStarTM": 2500,
        "hireTierScale": [1, 2, 4, 8, 16, 32, 64, 128],
    })

if __name__ == "__main__":
    save_json(GAME_DATA / "staff_roles.json", {"dataVersion": data_version(), "roles": roles})
    print("staff_roles.json dijana (5 peranan; gaji terikat tier)")
