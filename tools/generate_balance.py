#!/usr/bin/env python3
"""Jana game-data/balance.json - satu sumber kebenaran pemalar ekonomi."""
from common import (AUCTION_DURATION_H, AUCTION_FEE_PCT, AUCTION_START_PCT,
                    ACTIVE_H, COMPANY_COVERAGE, GAME_DATA,
                    LEVERAGE_INTEREST_WEEKLY_PCT, LEVERAGE_MAX_PCT,
                    LEGACY_PREMIUM_MAX, LEGACY_PREMIUM_MIN, NET_CONTRIB_PCT,
                    OFFLINE_CAP_H, RESPAWN_H, SALARY_SHARE, UPGRADE_COST_GROWTH,
                    data_version, save_json)

# LEVERAGE_CAP = had leverage 2x pendapatan harian bersih
LEVERAGE_CAP = 2.0

balance = {
    "dataVersion": data_version(),
    "auctionFeePct": AUCTION_FEE_PCT,                    # yuran lelongan 2%
    "auctionStartPctOfNT": AUCTION_START_PCT,            # mula lelongan 95% NT
    "leverageMaxPct": LEVERAGE_MAX_PCT,                  # leverage maks 40%
    "leverageInterestWeeklyPct": LEVERAGE_INTEREST_WEEKLY_PCT,  # faedah 8%/minggu
    "leverageCapDailyNetMultiplier": LEVERAGE_CAP,       # had = 2x pendapatan harian bersih
    "auctionDurationHours": AUCTION_DURATION_H,          # tempoh lelongan 8 jam
    "offlineCapHours": OFFLINE_CAP_H,                    # simpanan offline 8 jam
    "upgradeCostGrowth": UPGRADE_COST_GROWTH,            # kosisen kos naik taraf 1.15
    "purchasedCompanyNetContributionPct": NET_CONTRIB_PCT,  # sumbangan bersih 35%
    "lostTargetRespawnHours": RESPAWN_H,                 # sasaran kalah muncul semula 48 jam
    "legacyPremiumMinPct": LEGACY_PREMIUM_MIN,           # premium legacy 15-25%
    "legacyPremiumMaxPct": LEGACY_PREMIUM_MAX,
    "calibration": {
        "activeHoursPerDay": ACTIVE_H,                   # 16 jam terkutip sehari
        "salaryShareOfGrossPct": SALARY_SHARE * 100,     # gaji ~20% kasar
        "companyCoverageOfTargetPct": COMPANY_COVERAGE * 100,
        "opsCoverageOfTargetPct": 100,                   # keputusan tafsiran - docs/DECISIONS.md
        "tolerancePct": 15,
    },
    "currencies": [
        {"id": "tm", "nameKey": "ui.currency.tm.name", "descKey": "ui.currency.tm.desc", "premium": False},
        {"id": "dp", "nameKey": "ui.currency.dp.name", "descKey": "ui.currency.dp.desc", "premium": False},
        {"id": "km", "nameKey": "ui.currency.km.name", "descKey": "ui.currency.km.desc", "premium": True},
    ],
}

if __name__ == "__main__":
    save_json(GAME_DATA / "balance.json", balance)
    print("balance.json dijana")
