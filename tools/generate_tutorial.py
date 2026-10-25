#!/usr/bin/env python3
"""Jana game-data/tutorial.json - 10 langkah + starterGrant + sasaran starter.

10 langkah: namakan syarikat + sektor; tekan operasi; kutip + pendapatan
offline; upah pekerja; naik taraf ke peringkat 2; buka Pasar; beli syarikat
T1 pertama; skrin Naik Tier; pitch pelabur ringkas; sasaran mingguan +
notifikasi.

Sasaran starter BERSKRIP & DITANDA KHAS - TIDAK mengganggu formula normal
(lihat docs/DECISIONS.md): lelonganfeatured T1 tanpa bidaan AI selama 8
minit supaya pembelian pertama berlaku dalam 8 minit.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, data_version, save_json  # noqa: E402

STEPS = [
    ("tu_step_01", "naming_screen", "enter_name_and_sector", 2000),
    ("tu_step_02", "op_card_first", "tap_operation", 1000),
    ("tu_step_03", "collect_button", "tap_collect", 1000),
    ("tu_step_04", "staff_screen", "hire_staff", 1500),
    ("tu_step_05", "op_upgrade_button", "upgrade_to_level_2", 2000),
    ("tu_step_06", "market_button", "open_market", 0),
    ("tu_step_07", "auction_bid_button", "buy_first_company", 0),
    ("tu_step_08", "tier_screen", "view_tier_up", 0),
    ("tu_step_09", "pitch_button", "complete_pitch", 0),
    ("tu_step_10", "weekly_card", "view_weekly_target", 0),
]

steps = []
for i, (sid, ui, action, reward) in enumerate(STEPS, start=1):
    steps.append({
        "step": i,
        "id": sid,
        "titleKey": f"tu.{sid}.title",
        "descKey": f"tu.{sid}.desc",
        "uiElement": ui,
        "requiredAction": action,
        "rewardTM": reward,
    })

tutorial = {
    "dataVersion": data_version(),
    "steps": steps,
    "starterGrant": {
        "tm": 50000,
        "noteKey": "tu.starter.note",
    },
    "starterTarget": {
        "special": True,
        "featuredTier": 1,
        "maxStartPriceTM": 45000,
        "noAiBidsMinutes": 8,
        "firstPurchaseWithinMinutes": 8,
        "noteKey": "tu.starter.note",
    },
}

if __name__ == "__main__":
    save_json(GAME_DATA / "tutorial.json", tutorial)
    print("tutorial.json dijana (10 langkah; grant 50,000 TM; sasaran starter berskrip)")
