#!/usr/bin/env python3
"""Jana game-data/sectors.json - 3 sektor dengan pengganda M dan sinergi."""
from common import GAME_DATA, SECTOR_MULT, SECTOR_SYNERGY, data_version, save_json

sectors = [
    {
        "id": "app",
        "nameKey": "sec.app.name",
        "descKey": "sec.app.desc",
        "multiplier": SECTOR_MULT["app"],
        "synergySectors": SECTOR_SYNERGY["app"],
        "colorHex": "#4C7DF0",
    },
    {
        "id": "fnb",
        "nameKey": "sec.fnb.name",
        "descKey": "sec.fnb.desc",
        "multiplier": SECTOR_MULT["fnb"],
        "synergySectors": SECTOR_SYNERGY["fnb"],
        "colorHex": "#F09A4C",
    },
    {
        "id": "logistics",
        "nameKey": "sec.logistics.name",
        "descKey": "sec.logistics.desc",
        "multiplier": SECTOR_MULT["logistics"],
        "synergySectors": SECTOR_SYNERGY["logistics"],
        "colorHex": "#46B58A",
    },
]

if __name__ == "__main__":
    save_json(GAME_DATA / "sectors.json", {"dataVersion": data_version(), "sectors": sectors})
    print("sectors.json dijana")
