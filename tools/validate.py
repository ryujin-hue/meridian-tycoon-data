#!/usr/bin/env python3
"""Validator data Meridian Tycoon.

Guna:
  python tools/validate.py            # validasi semua fail yang wujud (mod dev)
  python tools/validate.py --strict   # semua 16 fail WAJIB wujud (mod release)
  python tools/validate.py --report   # jana reports/data_report.md

Keluar 0 jika lulus, 1 jika ada ralat. Amaran tidak gagalkan validasi tetapi
dilaporkan dalam reports/data_report.md.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsonschema import Draft7Validator  # noqa: E402
import common as C  # noqa: E402

DATA_FILES = [
    "balance", "tiers", "sectors", "operations", "companies", "ai_ceos",
    "staff_roles", "staff_pool", "research", "events", "seasons",
    "cosmetics", "milestones", "tutorial", "leaderboard_bots",
]

EXPECTED_COUNTS = {
    "tiers": 8, "sectors": 3, "operations": 24, "companies": 216,
    "ai_ceos": 7, "staff_roles": 5, "staff_pool": 100, "research": 12,
    "seasons": 6, "cosmetics": 44, "milestones": 30,
}
EVENT_COUNTS = {"stock_out": 12, "bidding_war": 8, "daily_contract": 30,
                "weekly_target": 12, "market_news": 60, "micro_event": 20}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Had panjang aksara mengikut pola kunci i18n (padanan pertama menang)
LIMIT_RULES = [
    (r"^ui\.btn\.", 16),
    (r"^news\.", 90),
    (r"^notif\..*\.(body|msg)$", 90),
    (r"^notif\..*\.title$", 28),
    (r"\.(name|title)$", 28),
    (r"\.(desc|history|bio|text|body|hint|note)$", 140),
    (r"^tip\.", 140),
    (r"^bid_report\.", 140),
]
DEFAULT_LIMIT = 140

# Senarai jenama/nama sebenar yang dilarang muncul (padanan perkataan penuh)
BRAND_BLOCKLIST = [
    "apple", "google", "samsung", "tesla", "microsoft", "amazon", "nvidia",
    "facebook", "netflix", "toyota", "honda", "coca", "pepsi", "nike",
    "adidas", "mcdonald", "starbucks", "gojek", "shopee", "lazada",
    "airasia", "petronas", "maybank", "cimb", "genting", "proton",
    "perodua", "telkom", "indosat", "garuda", "tokopedia", "bukalapak",
    "traveloka", "alfamart", "indomaret", "unilever", "nestle", "shell",
    "exxon", "oracle", "intel", "sony", "nintendo", "disney", "spotify",
    "uber", "grab", "maxis", "digi", "celcom", "zin", "meridian",
]


def key_limit(key: str) -> int:
    for pat, lim in LIMIT_RULES:
        if re.search(pat, key):
            return lim
    return DEFAULT_LIMIT


# Fail berbentuk objek pembungkus: {dataVersion, <field>: [...]}
FIELD = {
    "tiers": "tiers", "sectors": "sectors", "operations": "operations",
    "companies": "companies", "ai_ceos": "ceos", "staff_roles": "roles",
    "staff_pool": "staff", "research": "nodes", "seasons": "seasons",
    "cosmetics": "cosmetics", "milestones": "milestones",
}


class Checker:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict = {}

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def check_semver(ch: Checker, path: Path, data) -> None:
    v = data.get("dataVersion") if isinstance(data, dict) else None
    if not v or not SEMVER_RE.match(str(v)):
        ch.err(f"{path.name}: medan dataVersion tiada / bukan semver")


def load_or_skip(ch: Checker, path: Path, schema_name: str):
    spath = C.SCHEMA_DIR / f"{schema_name}.schema.json"
    if not path.exists():
        ch.warn(f"{path.name}: tiada (dijana kemudian)")
        return None
    try:
        data = C.load_json(path)
    except Exception as e:  # noqa: BLE001
        ch.err(f"{path.name}: JSON tidak sah ({e})")
        return None
    schema = C.load_json(spath)
    errs = sorted(Draft7Validator(schema).iter_errors(data), key=lambda e: e.path)
    for e in errs[:20]:
        loc = ".".join(str(p) for p in e.path) or "(akar)"
        ch.err(f"{path.name}[{loc}]: {e.message[:220]}")
    check_semver(ch, path, data)
    return data


# ------------------------------------------------------------ fail data --
def check_basic_list(ch: Checker, name: str, data, expected: int) -> list:
    if not isinstance(data, list):
        ch.err(f"{name}: bukan senarai")
        return []
    if len(data) != expected:
        ch.err(f"{name}: kiraan {len(data)} != {expected}")
    ids = [d.get("id") for d in data if isinstance(d, dict)]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        ch.err(f"{name}: ID pendua {sorted(dupes)[:5]}")
    ch.stats[f"count.{name}"] = len(data)
    return data


def check_balance(ch: Checker, bal) -> None:
    if bal is None:
        return
    exp = {
        "auctionFeePct": C.AUCTION_FEE_PCT, "auctionStartPctOfNT": C.AUCTION_START_PCT,
        "leverageMaxPct": C.LEVERAGE_MAX_PCT,
        "leverageInterestWeeklyPct": C.LEVERAGE_INTEREST_WEEKLY_PCT,
        "auctionDurationHours": C.AUCTION_DURATION_H, "offlineCapHours": C.OFFLINE_CAP_H,
        "upgradeCostGrowth": C.UPGRADE_COST_GROWTH,
        "purchasedCompanyNetContributionPct": C.NET_CONTRIB_PCT,
        "lostTargetRespawnHours": C.RESPAWN_H,
        "legacyPremiumMinPct": C.LEGACY_PREMIUM_MIN, "legacyPremiumMaxPct": C.LEGACY_PREMIUM_MAX,
    }
    for k, v in exp.items():
        if abs(bal.get(k, -1) - v) > 1e-9:
            ch.err(f"balance.json: {k}={bal.get(k)} sepatutnya {v}")


def check_tiers(ch: Checker, tiers) -> None:
    if tiers is None:
        return
    for t in tiers:
        n = C.TIER_NUM[t["id"]]
        if t["baseValueA"] != C.TIERS[n - 1][1]:
            ch.err(f"tiers: {t['id']} baseValueA != {C.TIERS[n-1][1]}")
        if t["targetDailyNetIncome"] != C.TIERS[n - 1][2]:
            ch.err(f"tiers: {t['id']} targetDailyNetIncome != {C.TIERS[n-1][2]}")
        if t["reputationThreshold"] != C.TIERS[n - 1][3]:
            ch.err(f"tiers: {t['id']} reputationThreshold != {C.TIERS[n-1][3]}")


def check_operations(ch: Checker, ops) -> None:
    if ops is None:
        return
    ids = [o["id"] for o in ops]
    for sec in C.SECTORS:
        for k in range(1, 9):
            if f"op_{sec}_{k}" not in ids:
                ch.err(f"operations: op_{sec}_{k} tiada")
    for o in ops:
        if o["unlockTier"] != int(o["id"].split("_")[-1]):
            ch.err(f"operations: {o['id']} unlockTier tak sepadan dengan ID")


def ops_daily_net_by_tier(ops) -> dict:
    """Pendapatan harian bersih operasi bagi setiap tier (model rujukan):
    L(k,T) = min(10, T-k+2); net = 0.8 (selepas gaji 20%) x 16 jam x jumlah sejam."""
    by_key = {(o["sector"], int(o["id"].split("_")[-1])): o for o in ops}
    out = {}
    for T in range(1, 9):
        total = 0.0
        for sec in C.SECTORS:
            for k in range(1, T + 1):
                o = by_key[(sec, k)]
                lvl = min(10, T - k + 2)
                total += o["baseIncomePerHour"] * (o["incomeGrowthPerLevel"] ** (lvl - 1))
        out[T] = 0.8 * C.ACTIVE_H * total
    return out


def check_ops_calibration(ch: Checker, ops, warnings_into_stats=False) -> dict:
    if ops is None:
        return {}
    res = {}
    daily = ops_daily_net_by_tier(ops)
    for T in range(1, 9):
        target = C.TIERS[T - 1][2]
        dev = (daily[T] - target) / target * 100.0
        res[T] = dev
        if abs(dev) > 15.0:
            ch.err(f"operations: pendapatan harian tier {T} menyimpang {dev:+.1f}% (>15%) dari sasaran")
        elif abs(dev) > 5.0:
            ch.warn(f"operations: pendapatan harian tier {T} menyimpang {dev:+.1f}% dari sasaran")
    ch.stats["ops_daily_dev_pct"] = {f"t{t}": round(v, 2) for t, v in res.items()}
    return res


def check_companies(ch: Checker, comps, ceos) -> None:
    if comps is None:
        return
    ceo_ids = {c["id"] for c in ceos} if ceos else set()
    per_tier_sector = defaultdict(int)
    legacy = 0
    for c in comps:
        cid = c["id"]
        n = c["tier"]
        M = C.SECTOR_MULT[c["sector"]]
        if c["category"] == "legacy":
            legacy += 1
            exp_nt = C.nt_value(C.TIERS[n - 1][1], c["grossIncomePerHourK"], c["reputation"], M)
            exp_price = C.start_price(exp_nt, c.get("premiumPct", 0))
        else:
            per_tier_sector[(n, c["sector"])] += 1
            if c["category"] != C.CATEGORY_BY_TIER[n]:
                ch.err(f"{cid}: kategori {c['category']} tak sepadan tier {n} (sepatutnya {C.CATEGORY_BY_TIER[n]})")
            exp_nt = C.nt_value(C.TIERS[n - 1][1], c["grossIncomePerHourK"], c["reputation"], M)
            exp_price = C.start_price(exp_nt)
        if c["ntValue"] != exp_nt:
            ch.err(f"{cid}: ntValue {c['ntValue']} != formula {exp_nt}")
        if c["auctionStartPriceTM"] != exp_price:
            ch.err(f"{cid}: harga mula {c['auctionStartPriceTM']} != 0.95xNT={exp_price}")
        exp_pb = round(C.payback_days(exp_price, c["grossIncomePerHourK"]), 2)
        if abs(c["paybackDays"] - exp_pb) > 0.02:
            ch.err(f"{cid}: payback {c['paybackDays']} != {exp_pb}")
        if c["synergySector"] == c["sector"]:
            ch.err(f"{cid}: synergySector tak boleh sama dengan sektor sendiri")
        if c["category"] == "legacy":
            if c.get("formerOwnerCeoId") not in ceo_ids:
                ch.err(f"{cid}: formerOwnerCeoId {c.get('formerOwnerCeoId')} tiada dalam ai_ceos")
            continue
        # Band payback (T2-T4: 10-20 hari; T5: 20-40 hari)
        for (lo_t, hi_t), (lo, hi) in C.PAYBACK_BAND.items():
            if lo_t <= n <= hi_t:
                if not (lo <= c["paybackDays"] <= hi):
                    ch.err(f"{cid}: payback {c['paybackDays']} di luar band {lo}-{hi} hari (T{n})")
    for (n, sec), cnt in sorted(per_tier_sector.items()):
        if cnt != 8:
            ch.err(f"companies: tier {n} sektor {sec} ada {cnt} (sepatutnya 8)")
    if legacy != 24:
        ch.err(f"companies: legacy ada {legacy} (sepatutnya 24)")
    ch.stats["companies.legacy"] = legacy
    ch.stats["companies.nt_by_tier"] = {}
    for n in range(1, 9):
        nts = sorted(c["ntValue"] for c in comps if c["tier"] == n and c["category"] != "legacy")
        pbs = sorted(c["paybackDays"] for c in comps if c["tier"] == n and c["category"] != "legacy")
        ch.stats["companies.nt_by_tier"][f"t{n}"] = {
            "min": nts[0], "median": nts[len(nts) // 2], "max": nts[-1],
            "payback_min": round(pbs[0], 1), "payback_median": round(pbs[len(pbs) // 2], 1),
            "payback_max": round(pbs[-1], 1),
        }
        cat = C.CATEGORY_BY_TIER[n]
        if cat in C.NT_GUIDE:
            lo, hi = C.NT_GUIDE[cat]
            if nts[-1] > hi:
                ch.warn(f"companies: NT maks tier {n} ({nts[-1]:,}) melebihi panduan {cat} {hi:,} (formula diutamakan)")
            if nts[0] < lo:
                ch.warn(f"companies: NT min tier {n} ({nts[0]:,}) bawah panduan {cat} {lo:,}")
    # NT mega: T6-T8 di luar panduan dijangka & dilaporkan
    for n in (7, 8):
        nts = [c["ntValue"] for c in comps if c["tier"] == n and c["category"] != "legacy"]
        if nts and min(nts) > C.NT_GUIDE["mega"][1]:
            ch.warn(f"companies: T{n} NT minimum {min(nts):,} > panduan mega 24,000,000 - "
                    f"secara matematik tidak dapat dielakkan (A={C.TIERS[n-1][1]:,}); lihat docs/ECONOMY_NOTES.md")


def check_formula_examples(ch: Checker) -> None:
    if not C.verify_nt_examples():
        ch.err("contoh rujukan NT GAGAL - formula tidak sepadan spesifikasi")


def check_cross_refs(ch: Checker, d: dict) -> None:
    def L(name):
        w = d.get(name)
        return w[FIELD[name]] if w else []

    sectors = {s["id"] for s in L("sectors")}
    tier_ids = {t["id"] for t in L("tiers")}
    ops = L("operations")
    if ops and sectors:
        for o in ops:
            if o["sector"] not in sectors:
                ch.err(f"operations: {o['id']} sektor {o['sector']} tiada")
    comps = L("companies")
    if comps and sectors:
        for c in comps:
            if c["sector"] not in sectors or c["synergySector"] not in sectors:
                ch.err(f"companies: {c['id']} rujukan sektor tidak sah")
    staff = L("staff_pool")
    roles = {r["id"] for r in L("staff_roles")}
    if staff and roles:
        for s in staff:
            if s["role"] not in roles:
                ch.err(f"staff_pool: {s['id']} peranan {s['role']} tiada")
    cos = {c["id"] for c in L("cosmetics")}
    if L("milestones") and cos:
        for m in L("milestones"):
            ref = m["reward"].get("cosmeticRef")
            if ref and ref not in cos:
                ch.err(f"milestones: {m['id']} cosmeticRef {ref} tiada")
    if L("seasons") and cos:
        for sn in L("seasons"):
            for tr in ("freeTrack", "premiumTrack"):
                for st in sn[tr]["steps"]:
                    for rw in st["rewards"]:
                        if rw["type"] == "cosmetic" and rw.get("ref") not in cos:
                            ch.err(f"seasons: {sn['id']} {tr} langkah {st['step']} rujukan {rw.get('ref')} tiada")
    if d.get("events") and sectors:
        for so in d["events"]["stock_out"]:
            if so["sector"] not in sectors:
                ch.err(f"events: {so['id']} sektor tiada")
    if d.get("tutorial"):
        st = d["tutorial"]["starterTarget"]
        comps_t1 = [c for c in comps if c["tier"] == 1 and c["category"] != "legacy"]
        if comps_t1:
            cheapest = min(c["auctionStartPriceTM"] for c in comps_t1)
            if d["tutorial"]["starterGrant"]["tm"] < cheapest * 1.1:
                ch.err(f"tutorial: starterGrant {d['tutorial']['starterGrant']['tm']} < 110% harga mula T1 termurah ({cheapest})")
            if st["maxStartPriceTM"] < cheapest:
                ch.err(f"tutorial: maxStartPriceTM {st['maxStartPriceTM']} < harga mula T1 termurah ({cheapest})")
    if d.get("leaderboard_bots") and tier_ids:
        for b in d["leaderboard_bots"]["bots"]:
            if f"t{b['tier']}" not in tier_ids:
                ch.err(f"leaderboard_bots: {b['id']} tier tidak sah")


# --------------------------------------------------------------- i18n --
def check_i18n(ch: Checker, langs: dict) -> None:
    if not langs:
        ch.warn("i18n: tiada fail lagi")
        return
    en = langs.get("en")
    if en is None:
        ch.err("i18n: en.json wajib wujud dahulu")
        return
    en_keys = set(en["strings"].keys())
    for lang, data in langs.items():
        keys = set(data["strings"].keys())
        if lang != "en":
            missing = en_keys - keys
            extra = keys - en_keys
            if missing:
                ch.err(f"i18n/{lang}.json: {len(missing)} kunci hilang (cth: {sorted(missing)[:5]})")
            if extra:
                ch.err(f"i18n/{lang}.json: {len(extra)} kunci berlebihan (cth: {sorted(extra)[:5]})")
    # Had panjang
    for lang, data in langs.items():
        over = []
        for k, v in data["strings"].items():
            lim = key_limit(k)
            if len(v) > lim:
                over.append(f"{k} ({len(v)}>{lim})")
        if over:
            ch.err(f"i18n/{lang}.json: {len(over)} kunci melebihi had (cth: {over[:5]})")
    ch.stats["i18n.keys"] = len(en_keys)
    # Unik: nama syarikat / bandar / person (st + ceo + lb.pool)
    def values_of(prefix):
        return [v for k, v in en["strings"].items() if k.startswith(prefix) and k.endswith(".name")]
    cats = {
        "syarikat (co.)": "co.", "bandar (city.)": "city.",
        "person (st/ceo/lb)": None,
    }
    person_vals = (values_of("st.") + values_of("ceo.") +
                   [v for k, v in en["strings"].items() if re.match(r"^lb\.(bot|pool)\.", k) and k.endswith(".name")])
    for label, vals in list(cats.items())[:-1] + [("person (st/ceo/lb)", person_vals)]:
        dupes = {v for v in vals if vals.count(v) > 1}
        if dupes:
            ch.err(f"i18n/en: nama pendua dalam {label}: {sorted(dupes)[:5]}")
    # Blok senarai jenama sebenar
    all_names = (values_of("co.") + values_of("city.") + values_of("st.") + values_of("ceo.") +
                 [v for k, v in en["strings"].items() if re.match(r"^lb\.(bot|pool)\.", k)])
    for v in all_names:
        low = v.lower()
        for b in BRAND_BLOCKLIST:
            if re.search(rf"\b{re.escape(b)}\b", low):
                ch.err(f"i18n/en: nama '{v}' menyerupai jenama terlarang '{b}'")
    # Semua kunci yang dirujuk oleh fail data wajib wujud dalam en
    referenced = set()
    for fname in DATA_FILES:
        path = C.GAME_DATA / f"{fname}.json"
        if not path.exists():
            continue
        data = C.load_json(path)
        if fname == "events":
            items2 = [x for g in data.values() if isinstance(g, list) for x in g]
        elif fname == "leaderboard_bots":
            items2 = data["bots"] + data["namePool"]
        elif fname == "balance":
            items2 = data.get("currencies", [])
        elif fname == "tutorial":
            items2 = data["steps"] + [data["starterGrant"], data["starterTarget"]]
        elif fname in FIELD:
            items2 = data[FIELD[fname]]
        else:
            items2 = [data]
        for obj in items2:
            if isinstance(obj, dict):
                for kk, vv in obj.items():
                    if kk.endswith("Key") and isinstance(vv, str) \
                            and kk not in ("statKey", "skillId"):
                        referenced.add(vv)
    missing = {k for k in referenced if k not in en_keys}
    if missing:
        ch.err(f"i18n/en: {len(missing)} kunci dirujuk data tapi tiada (cth: {sorted(missing)[:8]})")


# ------------------------------------------------------------- laporan --
def write_report(ch: Checker, d: dict) -> Path:
    C.REPORTS.mkdir(exist_ok=True)
    p = C.REPORTS / "data_report.md"
    lines = ["# Laporan Data Meridian Tycoon", "", f"Dijana oleh tools/validate.py (dataVersion {C.data_version()}).", ""]
    lines.append("## Bilangan Entiti")
    lines.append("")
    lines.append("| Fail | Bilangan | Sasaran |")
    lines.append("|---|---|---|")
    targets = {"tiers": 8, "sectors": 3, "operations": 24, "companies": 216, "ai_ceos": 7,
               "staff_roles": 5, "staff_pool": 100, "research": 12, "seasons": 6,
               "cosmetics": 44, "milestones": 30, "tutorial (langkah)": 10}
    for name, tgt in targets.items():
        key = name.split(" ")[0]
        cnt = ch.stats.get(f"count.{key}", "-")
        lines.append(f"| {key} | {cnt} | {tgt} |")
    lines.append(f"| leaderboard_bots | {ch.stats.get('count.leaderboard_bots', '-')} bot + 120 nama | 29 + 120 |")
    if d.get("events"):
        for g, tgt in EVENT_COUNTS.items():
            lines.append(f"| events.{g} | {len(d['events'].get(g, []))} | {tgt} |")
    lines.append("")
    if "companies.nt_by_tier" in ch.stats:
        lines.append("## Taburan NT & Payback mengikut Tier (syarikat bukan legacy)")
        lines.append("")
        lines.append("| Tier | NT min | NT median | NT maks | Payback min | Payback median | Payback maks |")
        lines.append("|---|---|---|---|---|---|---|")
        for t, s in ch.stats["companies.nt_by_tier"].items():
            lines.append(f"| {t} | {s['min']:,} | {s['median']:,} | {s['max']:,} | {s['payback_min']} | {s['payback_median']} | {s['payback_max']} |")
        lines.append("")
    if "ops_daily_dev_pct" in ch.stats:
        lines.append("## Penyimpangan Pendapatan Harian Operasi vs Sasaran Tier")
        lines.append("")
        lines.append("| Tier | Penyimpangan |")
        lines.append("|---|---|")
        for t, v in ch.stats["ops_daily_dev_pct"].items():
            lines.append(f"| {t} | {v:+.2f}% |")
        lines.append("")
    if ch.stats.get("i18n.keys"):
        lines.append(f"## i18n: {ch.stats['i18n.keys']} kunci (en = rujukan)")
        lines.append("")
    lines.append("## Amaran")
    lines.append("")
    if ch.warnings:
        lines += [f"- {w}" for w in ch.warnings]
    else:
        lines.append("- Tiada.")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="semua fail wajib wujud")
    ap.add_argument("--report", action="store_true", help="jana reports/data_report.md")
    args = ap.parse_args()

    ch = Checker()

    # Skema wajib lengkap sentiasa
    for f in DATA_FILES + ["i18n"]:
        if not (C.SCHEMA_DIR / f"{f}.schema.json").exists():
            ch.err(f"schema/{f}.schema.json tiada")

    d = {}
    for name in DATA_FILES:
        path = C.GAME_DATA / f"{name}.json"
        data = load_or_skip(ch, path, name)
        d[name] = data
        if args.strict and data is None:
            ch.err(f"{name}.json: WAJIB wujud (mod strict)")

    langs = {}
    for lang in ("en", "ms", "id"):
        p = C.I18N_DIR / f"{lang}.json"
        if p.exists():
            langs[lang] = load_or_skip(ch, p, "i18n")
        elif args.strict:
            ch.err(f"i18n/{lang}.json: WAJIB wujud (mod strict)")

    if d["balance"]:
        check_balance(ch, d["balance"])
    check_tiers(ch, d["tiers"]["tiers"] if d["tiers"] else None)
    check_operations(ch, d["operations"]["operations"] if d["operations"] else None)
    check_ops_calibration(ch, d["operations"]["operations"] if d["operations"] else None)
    check_companies(ch,
                    d["companies"]["companies"] if d["companies"] else None,
                    d["ai_ceos"]["ceos"] if d["ai_ceos"] else None)
    check_formula_examples(ch)
    check_cross_refs(ch, d)

    for name in ("sectors", "ai_ceos", "staff_roles", "staff_pool", "research",
                 "seasons", "cosmetics", "milestones", "tutorial", "leaderboard_bots"):
        if d[name] is None:
            continue
        if name == "leaderboard_bots":
            b = d[name]["bots"]
            ch.stats["count.leaderboard_bots"] = len(b)
            if len(b) != 29:
                ch.err(f"leaderboard_bots: {len(b)} bot != 29")
            if len(d[name]["namePool"]) != 120:
                ch.err("leaderboard_bots: kolam nama != 120")
        elif name == "tutorial":
            ch.stats["count.tutorial"] = len(d[name]["steps"])
            if len(d[name]["steps"]) != 10:
                ch.err("tutorial: langkah != 10")
        else:
            check_basic_list(ch, name, d[name][FIELD[name]], EXPECTED_COUNTS[name])

    check_i18n(ch, langs)

    # Laporan
    if args.report:
        rp = write_report(ch, d)
        print(f"Laporan: {rp}")

    print(f"Ralat: {len(ch.errors)} | Amaran: {len(ch.warnings)}")
    for e in ch.errors[:40]:
        print(f"  [RALAT] {e}")
    if len(ch.errors) > 40:
        print(f"  ... dan {len(ch.errors) - 40} ralat lagi")
    for w in ch.warnings[:15]:
        print(f"  [AMARAN] {w}")
    if len(ch.warnings) > 15:
        print(f"  ... dan {len(ch.warnings) - 15} amaran lagi")
    return 1 if ch.errors else 0


if __name__ == "__main__":
    sys.exit(main())
