#!/usr/bin/env python3
"""Jana game-data/companies.json - 216 syarikat.

192 biasa  = 8 sektor-tier x 3 sektor (8 setiap sektor setiap tier)
24 legacy  = 8 setiap sektor (asas tier 6/7/8) + formerOwnerCeoId + premiumPct

Formula (WAJIB, lihat common.py):
  NT   = A x (1 + 0.10 P + 0.005 R) x M
  Harga mula = 0.95 x NT (legacy + premium 15-25%)
  Payback    = harga mula / (0.35 x P x 1000 x 24)
  P daripada payback D: P = 0.95.A.M.(1+0.005R) / (D.8400 - 0.095.A.M)

Sasaran payback: T2-T4 10-20 hari, T5 20-40 hari (adaptif supaya NT kekal
dalam panduan). T6-T8: P dipilih untuk sumbangan pendapatan munasabah;
payback panjang dijangka & dilaporkan (lihat docs/ECONOMY_NOTES.md).
T1: D 15-25 hari (tiada band dalam spesifikasi - keputusan di DECISIONS.md).
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text_names as TN  # noqa: E402
from common import (GAME_DATA, NT_GUIDE, SECTOR_MULT, SECTORS, TIERS,  # noqa: E402
                    CATEGORY_BY_TIER, SEED, data_version, payback_days,
                    p_from_payback, nt_value, start_price, save_json)

rng = random.Random(SEED + 100)

REP_BAND = {1: (10, 25), 2: (20, 40), 3: (30, 50), 4: (45, 65),
            5: (55, 75), 6: (60, 80), 7: (60, 80), 8: (70, 90)}
P_RANGE = {6: (10.0, 18.0), 7: (14.0, 24.0), 8: (30.0, 45.0)}
STAFF_RANGE = {1: (5, 25), 2: (20, 80), 3: (60, 250), 4: (200, 800),
               5: (600, 2500), 6: (2000, 8000), 7: (6000, 25000),
               8: (20000, 80000)}
LEGACY_TIER_COUNT = {6: 3, 7: 3, 8: 2}  # setiap sektor -> 8 legacy


def target_D_band(tier: int):
    if tier == 1:
        return 15.0, 25.0
    if tier <= 4:
        return 10.5, 19.5
    return 21.0, 39.0


def compute_P(tier: int, R: int, M: float, sector: str, seq: int):
    """Kembalikan (P, D) mengikut peraturan tier."""
    a = TIERS[tier - 1][1]
    cat = CATEGORY_BY_TIER[tier]
    if tier <= 5:
        d_lo, d_hi = target_D_band(tier)
        D = d_lo + (d_hi - d_lo) * ((SEED + seq * 37 + tier * 101 + hash_slug(sector)) % 1000) / 1000.0
        P = p_from_payback(a, D, R, M)
        if tier == 5:  # adaptif: kekalkan NT <= 3M
            while nt_value(a, round(P, 2), R, M) > NT_GUIDE["rare"][1] and D < d_hi - 0.25:
                D = min(d_hi, D + 0.5)
                P = p_from_payback(a, D, R, M)
        if tier in (2, 3, 4):  # adaptif: kekalkan NT >= panduan bawah
            while nt_value(a, round(P, 2), R, M) < NT_GUIDE[cat][0] and D > d_lo + 0.25:
                D = max(d_lo, D - 0.5)
                P = p_from_payback(a, D, R, M)
        return round(P, 2), round(D, 2)
    p_lo, p_hi = P_RANGE[tier]
    P = round(p_lo + (p_hi - p_lo) * ((SEED + seq * 53 + tier * 77) % 1000) / 1000.0, 2)
    if tier == 7:  # kurangkan P jika NT melebihi panduan mega ( Formula menang; kurangkan bila boleh)
        while nt_value(a, P, R, M) > NT_GUIDE["mega"][1] and P > p_lo:
            P = round(max(p_lo, P * 0.93), 2)
            if P <= p_lo:
                break
    return P, None


def hash_slug(s: str) -> int:
    """Pengganti hash() yang stabil antara run."""
    return sum((i + 1) * ord(ch) for i, ch in enumerate(s))


def make_company(sector: str, tier: int, idx: int, kind: str, ceo_ids: list):
    a = TIERS[tier - 1][1]
    R = rng.randint(*REP_BAND[tier])
    M = SECTOR_MULT[sector]
    if kind == "legacy":
        R = rng.randint(75, 95)
    P, _D = compute_P(tier, R, M, sector, idx + tier * 10 + SECTORS.index(sector) * 100)
    nt = nt_value(a, P, R, M)
    premium = 0.0
    if kind == "legacy":
        premium = round(rng.uniform(15.0, 25.0), 1)
    price = start_price(nt, premium)
    pb = round(payback_days(price, P), 2)

    cid = (f"co_legacy_{sector}_{idx:02d}" if kind == "legacy"
           else f"co_{sector}_t{tier}_{idx:02d}")
    seq_key = (sector, tier if kind == "regular" else 0, idx)
    name = TN.company_name(sector, REG_SEQ[sector] if kind == "regular" else LEG_SEQ[sector],
                           "regular" if kind == "regular" else "legacy")
    if kind == "regular":
        REG_SEQ[sector] += 1
    else:
        LEG_SEQ[sector] += 1
    year = (rng.randint(1948, 1992) if kind == "legacy" else rng.randint(1972, 2024))
    staff = rng.randint(*STAFF_RANGE[tier])
    tags = rng.sample(TN.COMPANY_TAGS, rng.randint(2, 3))
    syn = rng.choice([s for s in SECTORS if s != sector])
    comp = {
        "id": cid,
        "nameKey": f"co.{cid}.name",
        "sector": sector,
        "tier": tier,
        "category": kind if kind == "legacy" else CATEGORY_BY_TIER[tier],
        "grossIncomePerHourK": P,
        "reputation": R,
        "foundedYear": year,
        "hqCityKey": TN.city_slug(rng.choice(TN.CITIES)),
        "staffCount": staff,
        "descKey": f"co.{cid}.desc",
        "historyKey": f"co.{cid}.history",
        "tags": tags,
        "synergySector": syn,
        "ntValue": nt,
        "auctionStartPriceTM": price,
        "paybackDays": pb,
    }
    if kind == "legacy":
        comp["formerOwnerCeoId"] = ceo_ids[0] if idx == 1 else rng.choice(ceo_ids)
        comp["premiumPct"] = premium
    NAME_MAP[comp["nameKey"]] = name
    return comp


NAME_MAP = {}
REG_SEQ = {s: 0 for s in SECTORS}
LEG_SEQ = {s: 0 for s in SECTORS}

if __name__ == "__main__":
    ceo_ids = [c["id"] for c in json.loads(
        (GAME_DATA / "ai_ceos.json").read_text(encoding="utf-8"))["ceos"]]
    boss = "ceo_victor_nyx"
    companies = []
    for tier in range(1, 9):
        for sector in SECTORS:
            for idx in range(1, 9):
                companies.append(make_company(sector, tier, idx, "regular", ceo_ids))
    for sector in SECTORS:
        idx = 0
        for ltier in (6, 7, 8):
            for _ in range(LEGACY_TIER_COUNT[ltier]):
                idx += 1
                companies.append(make_company(sector, ltier, idx, "legacy", [boss] + ceo_ids))
    save_json(GAME_DATA / "companies.json",
              {"dataVersion": data_version(), "companies": companies})
    (GAME_DATA.parent / "tools" / "generated").mkdir(exist_ok=True)
    (GAME_DATA.parent / "tools" / "generated" / "company_names.json").write_text(
        json.dumps(NAME_MAP, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"companies.json dijana: {len(companies)} syarikat "
          f"({sum(1 for c in companies if c['category'] != 'legacy')} biasa + "
          f"{sum(1 for c in companies if c['category'] == 'legacy')} legacy)")
