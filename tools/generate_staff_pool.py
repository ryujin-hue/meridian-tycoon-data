#!/usr/bin/env python3
"""Jana game-data/staff_pool.json - 100 individu rekaan.

5 peranan x 5 bintang x 4 individu = 100. Nama campuran Asia Tenggara +
antarabangsa daripada text_names.py (offset tetap 0-99 supaya deterministik
dan tidak bertindih dengan bot leaderboard).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text_names as TN  # noqa: E402
from common import GAME_DATA, data_version, save_json  # noqa: E402

ROLES = ["coo", "cfo", "cmo", "cto", "hr"]

staff = []
name_map = {}
i = 0
for role in ROLES:
    for star in range(1, 6):
        for n in range(1, 5):
            sid = f"st_{role}_{star}_{n}"
            key = f"st.{sid}.name"
            name = TN.person_name(TN.STAFF_OFFSET, i)
            name_map[key] = name
            staff.append({
                "id": sid,
                "role": role,
                "star": star,
                "nameKey": key,
                "bioKey": f"st.{sid}.bio",
            })
            i += 1

if __name__ == "__main__":
    save_json(GAME_DATA / "staff_pool.json", {"dataVersion": data_version(), "staff": staff})
    (GAME_DATA.parent / "tools" / "generated").mkdir(exist_ok=True)
    (GAME_DATA.parent / "tools" / "generated" / "staff_names.json").write_text(
        json.dumps(name_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"staff_pool.json dijana ({len(staff)} staf; nama unik: "
          f"{len(set(name_map.values())) == len(name_map)})")
