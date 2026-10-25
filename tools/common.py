#!/usr/bin/env python3
"""Pustaka kongsi Meridian Tycoon: formula ekonomi, pemalar, utiliti IO.

SEMUA formula mengikuti spesifikasi GDD - dilarang ubah tanpa kebenaran.
Jika ada ketidakkonsistenan, catat dalam docs/ECONOMY_NOTES.md.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME_DATA = ROOT / "game-data"
I18N_DIR = GAME_DATA / "i18n"
SCHEMA_DIR = ROOT / "schema"
REPORTS = ROOT / "reports"
DOCS = ROOT / "docs"

# Seed tetap global - penjanaan boleh diulang 100% (lihat docs/DECISIONS.md)
SEED = 20261025

DATA_VERSION_DEV = "0.9.0"
DATA_VERSION_RELEASE = "1.0.0"


def data_version() -> str:
    return os.environ.get("MT_DATA_VERSION", DATA_VERSION_DEV)


SECTORS = ["app", "fnb", "logistics"]
# Pengganda sektor M (julat dibenarkan 0.90-1.15)
SECTOR_MULT = {"app": 1.15, "fnb": 0.90, "logistics": 1.00}
SECTOR_SYNERGY = {
    "app": ["fnb", "logistics"],
    "fnb": ["app", "logistics"],
    "logistics": ["app", "fnb"],
}

# (id, A asas nilai, sasaran pendapatan harian bersih, ambang reputasi, ganjaran DP)
TIERS = [
    ("t1", 40_000, 6_000, None, None),
    ("t2", 80_000, 14_000, 10, 10),
    ("t3", 150_000, 32_000, 20, 20),
    ("t4", 400_000, 75_000, 35, 35),
    ("t5", 1_100_000, 170_000, 50, 50),
    ("t6", 3_000_000, 400_000, 60, 60),
    ("t7", 8_500_000, 950_000, 70, 70),
    ("t8", 24_000_000, 2_200_000, 80, 80),
]
TIER_NUM = {t[0]: i + 1 for i, t in enumerate(TIERS)}

CATEGORY_BY_TIER = {
    1: "starter", 2: "midmarket", 3: "midmarket",
    4: "rare", 5: "rare", 6: "mega", 7: "mega", 8: "mega",
}

# Julat NT panduan (formula yang menang; penyimpangan dilaporkan)
NT_GUIDE = {
    "midmarket": (80_000, 400_000),
    "rare": (400_000, 3_000_000),
    "mega": (3_000_000, 24_000_000),
}
# Sasaran payback (hari): T2-T4 10-20, T5 20-40. T1 & T6-T8: dilaporkan sahaja.
PAYBACK_BAND = {(2, 4): (10.0, 20.0), (5, 5): (20.0, 40.0)}

# Pemalar lelongan / ekonomi (mesti sepadan balance.json)
AUCTION_FEE_PCT = 2.0
AUCTION_START_PCT = 95.0
LEVERAGE_MAX_PCT = 40.0
LEVERAGE_INTEREST_WEEKLY_PCT = 8.0
AUCTION_DURATION_H = 8.0
OFFLINE_CAP_H = 8.0
UPGRADE_COST_GROWTH = 1.15
NET_CONTRIB_PCT = 35.0        # sumbangan bersih syarikat dibeli (asas payback)
RESPAWN_H = 48.0
LEGACY_PREMIUM_MIN = 15.0
LEGACY_PREMIUM_MAX = 25.0

# Andaian kalibrasi pemain aktif
ACTIVE_H = 16.0               # jam kutipan sehari
SALARY_SHARE = 0.20           # gaji harian ~ 20% pendapatan kasar
COMPANY_COVERAGE = 0.30       # syarikat dibeli menyumbang <= 30% sasaran


# ---------------------------------------------------------------- formula --
def nt_value(a: float, p: float, r: float, m: float) -> int:
    """NT = A x (1 + 0.10 x P + 0.005 x R) x M  (integer, dibundarkan)."""
    return round(a * (1 + 0.10 * p + 0.005 * r) * m)


def start_price(nt: int, premium_pct: float = 0.0) -> int:
    """Harga mula lelongan = 0.95 x NT (legacy ditambah premium)."""
    return round(nt * 0.95 * (1 + premium_pct / 100.0))


def payback_days(price: float, p: float) -> float:
    """Payback (hari) = harga mula / (0.35 x P x 1000 x 24)."""
    return price / (0.35 * p * 1000 * 24)


def p_from_payback(a: float, d: float, r: float, m: float) -> float:
    """P daripada sasaran payback D:
    P = 0.95.A.M.(1+0.005R) / (D.8400 - 0.095.A.M)
    """
    den = d * 8400 - 0.095 * a * m
    if den <= 0:
        raise ValueError(f"Payback D={d} mustahil untuk A={a}, M={m} (penyebut <= 0)")
    return 0.95 * a * m * (1 + 0.005 * r) / den


# Contoh rujukan yang WAJIB lulus (validator memeriksa secara eksak):
NT_EXAMPLES = [
    ((150_000, 2.4, 35, 1.10), 233_475),
    ((400_000, 5.2, 62, 0.95), 695_400),
    ((3_000_000, 14.0, 78, 1.25), 10_462_500),
]


def verify_nt_examples() -> bool:
    return all(nt_value(*args) == expected for args, expected in NT_EXAMPLES)


# ------------------------------------------------------------------- io --
def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def round_sig(x: float, sig: int = 3) -> float:
    """Bundar kepada n angka bererti (untuk kos yang kemas)."""
    if x == 0:
        return 0
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (sig - 1))


# ----------------------------------------------------------------- id --
ID_RE = {
    "co": re.compile(r"^co_[a-z0-9_]+$"),
    "ceo": re.compile(r"^ceo_[a-z0-9_]+$"),
    "st": re.compile(r"^st_(coo|cfo|cmo|cto|hr)_[1-5]_[1-4]$"),
    "rs": re.compile(r"^rs_(op|mk|mg)_[1-4]$"),
    "ev": re.compile(r"^ev_[a-z0-9_]+$"),
    "sn": re.compile(r"^sn_[1-6]$"),
    "cs": re.compile(r"^cs_(logo|hq|title)_[0-9]{2}$"),
    "ms": re.compile(r"^ms_[a-z0-9_]+$"),
    "op": re.compile(r"^op_(app|fnb|logistics)_[1-8]$"),
}
