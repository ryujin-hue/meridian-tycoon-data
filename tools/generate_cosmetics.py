#!/usr/bin/env python3
"""Jana game-data/cosmetics.json - 44 kosmetik: 12 kulit logo, 8 tema markas,
24 gelaran CEO (termasuk satu gelaran bagi setiap tier).

Harga KM tetap & jelas; kelangkaan TETAP (label), bukan berasaskan peluang.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, data_version, save_json  # noqa: E402

cosmetics = []

# 12 kulit logo (KM 40-120)
LOGO_RARITY = ["common"] * 4 + ["rare"] * 5 + ["epic"] * 3
LOGO_PRICE = [40, 45, 50, 60, 65, 70, 80, 90, 95, 110, 115, 120]
for i in range(1, 13):
    cosmetics.append({
        "id": f"cs_logo_{i:02d}",
        "type": "logo_skin",
        "nameKey": f"cs.cs_logo_{i:02d}.name",
        "descKey": f"cs.cs_logo_{i:02d}.desc",
        "fixedRarity": LOGO_RARITY[i - 1],
        "priceKM": LOGO_PRICE[i - 1],
        "tierRef": None,
    })

# 8 tema markas (KM 80-200)
HQ_PRICE = [80, 90, 100, 120, 140, 160, 180, 200]
HQ_RARITY = ["common", "common", "rare", "rare", "rare", "epic", "epic", "epic"]
for i in range(1, 9):
    cosmetics.append({
        "id": f"cs_hq_{i:02d}",
        "type": "hq_theme",
        "nameKey": f"cs.cs_hq_{i:02d}.name",
        "descKey": f"cs.cs_hq_{i:02d}.desc",
        "fixedRarity": HQ_RARITY[i - 1],
        "priceKM": HQ_PRICE[i - 1],
        "tierRef": None,
    })

# 24 gelaran CEO (KM 30-150); cs_title_01..08 = gelaran tier 1-8
TITLE_PRICE = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85,
               90, 100, 110, 120, 125, 130, 135, 140, 145, 148, 150, 150]
for i in range(1, 25):
    cosmetics.append({
        "id": f"cs_title_{i:02d}",
        "type": "ceo_title",
        "nameKey": f"cs.cs_title_{i:02d}.name",
        "descKey": f"cs.cs_title_{i:02d}.desc",
        "fixedRarity": "common" if i <= 8 else ("rare" if i <= 16 else "epic"),
        "priceKM": TITLE_PRICE[i - 1],
        "tierRef": i if i <= 8 else None,
    })

if __name__ == "__main__":
    save_json(GAME_DATA / "cosmetics.json", {"dataVersion": data_version(), "cosmetics": cosmetics})
    print(f"cosmetics.json dijana ({len(cosmetics)} kosmetik; harga KM tetap)")
