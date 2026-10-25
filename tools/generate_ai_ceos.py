#!/usr/bin/env python3
"""Jana game-data/ai_ceos.json - 7 profil CEO AI yang membida dalam lelongan.

Profil wajib: agresif, kalkulatif, opportunis, pesimis (sekurang-kurangnya
satu setiap satu). Satu CEO bertanda auctionBoss untuk sasaran legacy.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text_names as TN  # noqa: E402
from common import GAME_DATA, data_version, save_json  # noqa: E402

CEOS = [
    {
        "id": "ceo_rohan_vex", "profile": "agresif",
        "aggression": 0.90, "maxPremiumOverNT": 0.30, "bidIncrementPct": 6.0,
        "entryDelayMinutes": 10, "favoriteSectors": ["app", "logistics"],
        "tierSpeed": "fast", "auctionBoss": False,
    },
    {
        "id": "ceo_danil_wang", "profile": "agresif",
        "aggression": 0.80, "maxPremiumOverNT": 0.25, "bidIncrementPct": 5.0,
        "entryDelayMinutes": 20, "favoriteSectors": ["fnb", "logistics"],
        "tierSpeed": "fast", "auctionBoss": False,
    },
    {
        "id": "ceo_tariq_halim", "profile": "kalkulatif",
        "aggression": 0.40, "maxPremiumOverNT": 0.12, "bidIncrementPct": 3.0,
        "entryDelayMinutes": 45, "favoriteSectors": ["logistics"],
        "tierSpeed": "steady", "auctionBoss": False,
    },
    {
        "id": "ceo_sasha_kwan", "profile": "kalkulatif",
        "aggression": 0.35, "maxPremiumOverNT": 0.10, "bidIncrementPct": 3.0,
        "entryDelayMinutes": 60, "favoriteSectors": ["app"],
        "tierSpeed": "steady", "auctionBoss": False,
    },
    {
        "id": "ceo_maya_rin", "profile": "opportunis",
        "aggression": 0.65, "maxPremiumOverNT": 0.20, "bidIncrementPct": 4.0,
        "entryDelayMinutes": 25, "favoriteSectors": ["fnb", "app"],
        "tierSpeed": "fast", "auctionBoss": False,
    },
    {
        "id": "ceo_laila_suri", "profile": "pesimis",
        "aggression": 0.20, "maxPremiumOverNT": 0.05, "bidIncrementPct": 2.0,
        "entryDelayMinutes": 90, "favoriteSectors": ["fnb"],
        "tierSpeed": "slow", "auctionBoss": False,
    },
    {
        "id": "ceo_victor_nyx", "profile": "opportunis",
        "aggression": 0.70, "maxPremiumOverNT": 0.35, "bidIncrementPct": 5.0,
        "entryDelayMinutes": 5, "favoriteSectors": ["app", "fnb", "logistics"],
        "tierSpeed": "fast", "auctionBoss": True,
    },
]

for c in CEOS:
    c["nameKey"] = f"ceo.{c['id']}.name"
    c["bioKey"] = f"ceo.{c['id']}.bio"

if __name__ == "__main__":
    save_json(GAME_DATA / "ai_ceos.json", {"dataVersion": data_version(), "ceos": CEOS})
    # Simpan nama untuk i18n (Fasa F) - konsisten dengan text_names.py
    names = {f"ceo.{c['id']}.name": TN.CEO_NAMES[c["id"]] for c in CEOS}
    bios = {f"ceo.{c['id']}.bio": None for c in CEOS}
    (GAME_DATA.parent / "tools" / "generated").mkdir(exist_ok=True)
    import json
    (GAME_DATA.parent / "tools" / "generated" / "ceo_names.json").write_text(
        json.dumps(names, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ai_ceos.json dijana (7 CEO; 4 profil; boss: ceo_victor_nyx)")
