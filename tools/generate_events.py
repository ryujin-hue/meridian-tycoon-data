#!/usr/bin/env python3
"""Jana game-data/events.json:
- Habis Stok x12 (4 setiap sektor)
- Templat Perang Bidaan x8
- Kontrak harian x30
- Sasaran mingguan x12
- Berita pasar x60
- Mikro-event x20

Peraturan: setiap event ada tempoh + kesan angka; ganjaran hanya TM/DP/
kosmetik kecil; TIADA kesan yang menjadi syarat naik tier.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import GAME_DATA, SECTORS, SEED, TIERS, data_version, save_json  # noqa: E402

rng = random.Random(SEED + 300)

# ------------------------------------------------------------- stock out --
stock_out = []
for sec in SECTORS:
    for i in range(1, 5):
        stock_out.append({
            "id": f"ev_stockout_{sec}_{i}",
            "sector": sec,
            "titleKey": f"ev.ev_stockout_{sec}_{i}.title",
            "descKey": f"ev.ev_stockout_{sec}_{i}.desc",
            "durationHours": round(rng.uniform(2, 6), 1),
            "incomePenaltyPct": rng.choice([20, 25, 30, 35, 40]),
        })

# ----------------------------------------------------------- bidding war --
bidding_war = []
for i in range(1, 9):
    bidding_war.append({
        "id": f"ev_bidwar_{i}",
        "titleKey": f"ev.ev_bidwar_{i}.title",
        "descKey": f"ev.ev_bidwar_{i}.desc",
        "durationHours": rng.choice([2, 3, 4, 6, 8]),
        "extraCompetitorCount": rng.choice([1, 1, 2]),
        "aggressionBoostPct": rng.choice([10, 15, 20, 25]),
    })

# -------------------------------------------------------- daily contract --
# amaun collect_income mengikut band (T1-2, T3-4, T5-6, T7-8):
BAND_INCOME = {1: 8_000, 2: 40_000, 3: 250_000, 4: 1_200_000}
GOAL_TYPES = ["collect_income", "win_auction", "upgrade_operations",
              "hire_staff", "gain_reputation", "complete_contracts"]


def goal_for(band: int, gtype: str) -> int:
    if gtype == "collect_income":
        return BAND_INCOME[band]
    if gtype == "win_auction":
        return rng.choice([1, 1, 2])
    if gtype == "upgrade_operations":
        return rng.choice([2, 3, 4, 5, 6])
    if gtype == "hire_staff":
        return rng.choice([1, 2, 3])
    if gtype == "gain_reputation":
        return rng.choice([3, 5, 8, 10])
    return rng.choice([2, 3])


def reward_for(band: int, gtype: str):
    tm = int(BAND_INCOME[band] * rng.uniform(0.15, 0.25) // 100 * 100)
    dp = 0 if gtype != "collect_income" else rng.choice([0, 1, 2])
    return tm, dp


daily_contract = []
band_cycle = [1] * 8 + [2] * 8 + [3] * 7 + [4] * 7
for i in range(1, 31):
    band = band_cycle[i - 1]
    gtype = GOAL_TYPES[(i - 1) % len(GOAL_TYPES)]
    amt = goal_for(band, gtype)
    tm, dp = reward_for(band, gtype)
    sector = rng.choice(SECTORS + ["any"])
    daily_contract.append({
        "id": f"ev_contract_{i:02d}",
        "tierBand": band,
        "sector": sector,
        "titleKey": f"ev.ev_contract_{i:02d}.title",
        "descKey": f"ev.ev_contract_{i:02d}.desc",
        "durationHours": 24,
        "goal": {"type": gtype, "amount": amt},
        "reward": {"tm": tm, "dp": dp},
    })

# --------------------------------------------------------- weekly target --
weekly_target = []
WEEKLY_INCOME = {1: 40_000, 2: 200_000, 3: 1_200_000, 4: 6_000_000}
WEEKLY_REWARD_DP = {1: (8, 12), 2: (12, 20), 3: (20, 35), 4: (30, 50)}
COS_REFS = [f"cs_title_{n:02d}" for n in range(9, 17)] + [f"cs_logo_{n:02d}" for n in range(1, 5)]
wband_cycle = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
for i in range(1, 13):
    band = wband_cycle[i - 1]
    gtype = GOAL_TYPES[i % len(GOAL_TYPES)]
    if gtype == "collect_income":
        amt = WEEKLY_INCOME[band]
    elif gtype == "win_auction":
        amt = rng.choice([3, 4, 5])
    elif gtype == "upgrade_operations":
        amt = rng.choice([10, 14, 18])
    elif gtype == "hire_staff":
        amt = rng.choice([5, 7, 9])
    elif gtype == "gain_reputation":
        amt = rng.choice([15, 20, 25])
    else:
        amt = rng.choice([8, 10, 12])
    lo, hi = WEEKLY_REWARD_DP[band]
    dp = rng.randint(lo, hi)
    ref = COS_REFS[(i - 1) % len(COS_REFS)] if i % 3 == 0 else None
    weekly_target.append({
        "id": f"ev_weekly_{i:02d}",
        "tierBand": band,
        "titleKey": f"ev.ev_weekly_{i:02d}.title",
        "descKey": f"ev.ev_weekly_{i:02d}.desc",
        "durationHours": 168,
        "goal": {"type": gtype, "amount": amt},
        "reward": {"dp": dp, "cosmeticRef": ref},
    })

# ------------------------------------------------------------ market news --
market_news = []
scopes = ["global"] * 20 + ["app"] * 14 + ["fnb"] * 13 + ["logistics"] * 13
rng.shuffle(scopes)
for i in range(1, 61):
    scope = scopes[i - 1]
    effect = None
    if rng.random() < 0.55:
        effect = {
            "incomePercentPct": round(rng.uniform(2, 5), 1) * rng.choice([1, -1]),
            "durationHours": rng.choice([4, 6, 8, 12]),
        }
    market_news.append({
        "id": f"ev_news_{i:03d}",
        "scope": scope,
        "titleKey": f"news.ev_news_{i:03d}",
        "effect": effect,
        "weight": rng.randint(1, 5),
    })

# ------------------------------------------------------------ micro event --
micro_event = []
for i in range(1, 21):
    etype = rng.choice(["income_percent", "income_percent", "tm_bonus", "reputation_boost"])
    if etype == "income_percent":
        val = round(rng.uniform(3, 8), 1) * rng.choice([1, -1])
    elif etype == "tm_bonus":
        val = rng.choice([500, 1000, 2000, 3500, 5000])
    else:
        val = rng.choice([1, 2, 3])
    micro_event.append({
        "id": f"ev_micro_{i:02d}",
        "titleKey": f"ev.ev_micro_{i:02d}.title",
        "descKey": f"ev.ev_micro_{i:02d}.desc",
        "durationMinutes": rng.choice([15, 20, 30, 45, 60]),
        "effect": {"type": etype, "value": val},
        "weight": rng.randint(2, 6),
    })

events = {
    "dataVersion": data_version(),
    "stock_out": stock_out,
    "bidding_war": bidding_war,
    "daily_contract": daily_contract,
    "weekly_target": weekly_target,
    "market_news": market_news,
    "micro_event": micro_event,
}

if __name__ == "__main__":
    save_json(GAME_DATA / "events.json", events)
    print("events.json dijana:", {k: len(v) for k, v in events.items() if isinstance(v, list)})
