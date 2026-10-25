#!/usr/bin/env python3
"""Jana game-data/i18n/{en,ms,id}.json daripada data + modul teks.

- Nama (syarikat, bandar, staf, CEO, bot) ialah khas nama - nilai sama
  dalam ketiga-tiga bahasa (kunci tetap wujud dalam semua fail).
- Templat berslot diisi daripada data sebenar supaya teks sepadan realiti.
- Pariti kunci dijamin & disemak; had panjang disemak sebelum tulis.
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "i18n_text"))
import common as C  # noqa: E402
import ui as M_UI  # noqa: E402
import world as M_WORLD  # noqa: E402
import entities as M_ENT  # noqa: E402
import events_text as M_EV  # noqa: E402
import misc_text as M_MISC  # noqa: E402
import tips_text as M_TIPS  # noqa: E402
import text_names as TN  # noqa: E402
from validate import key_limit  # noqa: E402

LANGS = ("en", "ms", "id")
GEN = C.ROOT / "tools" / "generated"


def load(name, field=None):
    p = C.GAME_DATA / f"{name}.json"
    d = C.load_json(p)
    return d[field] if field else d


def stable(s: str) -> int:
    return sum((i + 1) * ord(ch) for i, ch in enumerate(s))


def fmt_num(x) -> str:
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    if isinstance(x, int):
        return f"{x:,}"
    return f"{x:g}"


def main() -> None:
    out = {lang: {} for lang in LANGS}

    def put(key: str, en: str, ms: str, vid: str) -> None:
        out["en"][key] = en
        out["ms"][key] = ms
        out["id"][key] = vid

    def put_all(key: str, value: str) -> None:  # nama khas - sama semua bahasa
        put(key, value, value, value)

    # ------------------------------------------------ modul statik ----
    for mod in (M_UI.STR, M_WORLD.STR, M_EV.STR, M_MISC.STR, M_TIPS.STR):
        for lang in LANGS:
            out[lang].update(mod[lang])
    for lang in LANGS:
        out[lang].update(M_WORLD.CITY_STR[lang])

    # ---------------------------------------------------------- data ----
    companies = load("companies", "companies")
    ceos = load("ai_ceos", "ceos")
    staff = load("staff_pool", "staff")
    ops = load("operations", "operations")
    tiers = load("tiers", "tiers")
    research = load("research", "nodes")
    events = load("events")
    cosmetics = load("cosmetics", "cosmetics")
    milestones = load("milestones", "milestones")
    tutorial = load("tutorial")
    lb = load("leaderboard_bots")
    roles = load("staff_roles", "roles")

    comp_names = json.loads((GEN / "company_names.json").read_text(encoding="utf-8"))
    ceo_names = json.loads((GEN / "ceo_names.json").read_text(encoding="utf-8"))
    staff_names = json.loads((GEN / "staff_names.json").read_text(encoding="utf-8"))
    bot_names = json.loads((GEN / "bot_names.json").read_text(encoding="utf-8"))

    ceo_name_by_id = {c["id"]: comp_names_key for c in ceos
                      for comp_names_key in [ceo_names[f"ceo.{c['id']}.name"]]}

    # Nama syarikat + bandar (khas nama)
    for key, name in comp_names.items():
        put_all(key, name)
    for key, name in staff_names.items():
        put_all(key, name)
    for key, name in bot_names.items():
        put_all(key, name)
    for key, name in ceo_names.items():
        put_all(key, name)
    for c in TN.CITIES:
        put_all(TN.city_slug(c), c)

    # -------------------------------------- penerangan & sejarah syarikat ----
    for co in companies:
        cid = co["id"]
        cat = co["category"] if co["category"] == "legacy" else "mega" \
            if co["category"] == "mega" else co["category"]
        band = {"starter": "starter", "midmarket": "midmarket",
                "rare": "rare", "mega": "mega", "legacy": "mega"}[co["category"]]
        rng = random.Random(C.SEED + stable(cid))
        trait = M_ENT.TRAITS[co["sector"]]["en"] and \
            {l: M_ENT.TRAITS[co["sector"]][l][rng.randrange(8)] for l in LANGS}
        city_name = out["en"][co["hqCityKey"]]
        tpl = M_ENT.DESC_TPL[co["sector"]][band]
        put(co["descKey"],
            tpl["en"].format(trait=trait["en"], city=city_name, year=co["foundedYear"]),
            tpl["ms"].format(trait=trait["ms"], city=city_name, year=co["foundedYear"]),
            tpl["id"].format(trait=trait["id"], city=city_name, year=co["foundedYear"]))
        origin = {l: M_ENT.ORIGINS[l][rng.randrange(8)] for l in LANGS}
        ev = {l: M_ENT.EVENTS[l][rng.randrange(8)] for l in LANGS}
        decade = (co["foundedYear"] // 10) % 10 * 10
        legacy_sfx = {"en": "", "ms": "", "id": ""}
        if co["category"] == "legacy":
            ceo_nm = ceo_name_by_id[co["formerOwnerCeoId"]]
            close_year = min(2024, co["foundedYear"] + rng.randrange(25, 70))
            legacy_sfx = {
                "en": M_ENT.LEGACY_SUFFIX["en"].format(close_year=close_year, ceo=ceo_nm),
                "ms": M_ENT.LEGACY_SUFFIX["ms"].format(close_year=close_year, ceo=ceo_nm),
                "id": M_ENT.LEGACY_SUFFIX["id"].format(close_year=close_year, ceo=ceo_nm),
            }
        htpl = M_ENT.HISTORY_TPL
        put(co["historyKey"],
            htpl["en"].format(origin=origin["en"], event=ev["en"], decade=decade, legacy=legacy_sfx["en"]),
            htpl["ms"].format(origin=origin["ms"], event=ev["ms"], decade=decade, legacy=legacy_sfx["ms"]),
            htpl["id"].format(origin=origin["id"], event=ev["id"], decade=decade, legacy=legacy_sfx["id"]))

    # ---------------------------------------------------------- bio CEO ----
    for cid, bio in M_ENT.CEO_BIOS.items():
        put(f"ceo.{cid}.bio", bio["en"], bio["ms"], bio["id"])

    # --------------------------------------------------------- bio staf ----
    def band(star: int) -> str:
        return "low" if star <= 2 else ("mid" if star == 3 else "high")

    for s in staff:
        rng = random.Random(C.SEED + stable(s["id"]))
        trait = M_ENT.STAFF_TRAITS["en"][rng.randrange(8)]
        trait_ms = M_ENT.STAFF_TRAITS["ms"][rng.randrange(8)]
        trait_id = M_ENT.STAFF_TRAITS["id"][rng.randrange(8)]
        tpl = M_ENT.STAFF_TPL[s["role"]][band(s["star"])]
        put(s["bioKey"],
            tpl["en"].format(trait=trait),
            tpl["ms"].format(trait=trait_ms),
            tpl["id"].format(trait=trait_id))

    # ---------------------------------------------------- ganjaran tier ----
    for t in tiers:
        if t["rewardKey"]:
            dp = fmt_num(t["tierUpRewardDP"])
            put(t["rewardKey"],
                M_WORLD.STR["en"][t["rewardKey"]].replace("{dp}", dp),
                M_WORLD.STR["ms"][t["rewardKey"]].replace("{dp}", dp),
                M_WORLD.STR["id"][t["rewardKey"]].replace("{dp}", dp))

    # ------------------------------------------------- penyelidikan ----
    for r in research:
        stage = str(r["stage"])
        val = fmt_num(r["effect"]["perStageValue"])
        k = r["descKey"]
        put(k,
            M_WORLD.STR["en"][k].format(stage=stage, val=val),
            M_WORLD.STR["ms"][k].format(stage=stage, val=val),
            M_WORLD.STR["id"][k].format(stage=stage, val=val))

    # ---------------------------------------------------- peranan ----
    for r in roles:
        pk = r["passive"]["descKey"]
        per, cap = fmt_num(r["passive"]["perStarPct"]), fmt_num(r["passive"]["hardCapPct"])
        put(pk,
            M_WORLD.STR["en"][pk].format(per=per, cap=cap),
            M_WORLD.STR["ms"][pk].format(per=per, cap=cap),
            M_WORLD.STR["id"][pk].format(per=per, cap=cap))
        # name/desc/active keys sudah statik dalam world.py

    # --------------------------------------------------- kosmetik ----
    for c in cosmetics:
        if c["tierRef"]:
            k = "cs.title.tier.desc"
            put(c["descKey"],
                M_MISC.STR["en"][k].format(n=c["tierRef"]),
                M_MISC.STR["ms"][k].format(n=c["tierRef"]),
                M_MISC.STR["id"][k].format(n=c["tierRef"]))
        else:
            kind = {"logo_skin": "logo", "hq_theme": "hq", "ceo_title": "title"}[c["type"]]
            k = f"cs.{kind}.desc"
            put(c["descKey"], M_MISC.STR["en"][k], M_MISC.STR["ms"][k], M_MISC.STR["id"][k])

    # --------------------------------------------------- milestone ----
    for m in milestones:
        g = m["goal"]
        k = f"ms.goal.{g['type']}"
        val = fmt_num(g["value"])
        sector = g.get("sector") or ""
        put(m["descKey"],
            M_MISC.STR["en"][k].format(value=val, sector=sector),
            M_MISC.STR["ms"][k].format(value=val, sector=sector),
            M_MISC.STR["id"][k].format(value=val, sector=sector))

    # ------------------------------------------------------- events ----
    sec_name = {lang: {} for lang in LANGS}
    for lang in LANGS:
        for sid in C.SECTORS:
            sec_name[lang][sid] = M_WORLD.STR[lang][f"sec.{sid}.name"]

    for ev in events["stock_out"]:
        n = int(ev["id"].split("_")[-1])
        tk = f"ev.stockout.{ev['sector']}.{n}.title"
        put(ev["titleKey"],
            M_EV.STR["en"][tk], M_EV.STR["ms"][tk], M_EV.STR["id"][tk])
        k = "ev.stockout.desc"
        sector = {l: sec_name[l][ev["sector"]] for l in LANGS}
        put(ev["descKey"],
            M_EV.STR["en"][k].format(sector=sector["en"], pct=fmt_num(ev["incomePenaltyPct"]), hours=fmt_num(ev["durationHours"])),
            M_EV.STR["ms"][k].format(sector=sector["ms"], pct=fmt_num(ev["incomePenaltyPct"]), hours=fmt_num(ev["durationHours"])),
            M_EV.STR["id"][k].format(sector=sector["id"], pct=fmt_num(ev["incomePenaltyPct"]), hours=fmt_num(ev["durationHours"])))

    for ev in events["bidding_war"]:
        tk = f"ev.bidwar.{int(ev['id'].split('_')[-1])}.title"
        put(ev["titleKey"],
            M_EV.STR["en"][tk], M_EV.STR["ms"][tk], M_EV.STR["id"][tk])
        k = "ev.bidwar.desc"
        put(ev["descKey"],
            M_EV.STR["en"][k].format(extra=ev["extraCompetitorCount"], pct=fmt_num(ev["aggressionBoostPct"]), hours=fmt_num(ev["durationHours"])),
            M_EV.STR["ms"][k].format(extra=ev["extraCompetitorCount"], pct=fmt_num(ev["aggressionBoostPct"]), hours=fmt_num(ev["durationHours"])),
            M_EV.STR["id"][k].format(extra=ev["extraCompetitorCount"], pct=fmt_num(ev["aggressionBoostPct"]), hours=fmt_num(ev["durationHours"])))

    for ev in events["daily_contract"]:
        g = ev["goal"]["type"]
        tk = f"ev.contract.{g}.title"
        put(ev["titleKey"],
            M_EV.STR["en"][tk], M_EV.STR["ms"][tk], M_EV.STR["id"][tk])
        k = f"ev.contract.{g}.desc"
        amt, tm, dp = fmt_num(ev["goal"]["amount"]), fmt_num(ev["reward"]["tm"]), fmt_num(ev["reward"]["dp"])
        put(ev["descKey"],
            M_EV.STR["en"][k].format(amount=amt, tm=tm, dp=dp),
            M_EV.STR["ms"][k].format(amount=amt, tm=tm, dp=dp),
            M_EV.STR["id"][k].format(amount=amt, tm=tm, dp=dp))

    for ev in events["weekly_target"]:
        g = ev["goal"]["type"]
        tk = f"ev.weekly.{g}.title"
        put(ev["titleKey"],
            M_EV.STR["en"][tk], M_EV.STR["ms"][tk], M_EV.STR["id"][tk])
        k = f"ev.weekly.{g}.desc"
        amt, dp = fmt_num(ev["goal"]["amount"]), fmt_num(ev["reward"]["dp"])
        put(ev["descKey"],
            M_EV.STR["en"][k].format(amount=amt, dp=dp),
            M_EV.STR["ms"][k].format(amount=amt, dp=dp),
            M_EV.STR["id"][k].format(amount=amt, dp=dp))

    for i, ev in enumerate(events["micro_event"]):
        et = ev["effect"]["type"]
        val = ev["effect"]["value"]
        if et == "income_percent":
            variant = "up" if val > 0 else "down"
            idx = 1 if i % 2 == 0 else 2
            tk = f"ev.micro.{variant}{idx}.title"
            dk = f"ev.micro.{variant}.desc"
        elif et == "tm_bonus":
            tk = f"ev.micro.tm{1 if i % 2 == 0 else 2}.title"
            dk = "ev.micro.tm.desc"
        else:
            tk = f"ev.micro.rep{1 if i % 2 == 0 else 2}.title"
            dk = "ev.micro.rep.desc"
        put(ev["titleKey"],
            M_EV.STR["en"][tk], M_EV.STR["ms"][tk], M_EV.STR["id"][tk])
        put(ev["descKey"],
            M_EV.STR["en"][dk].format(value=fmt_num(abs(val)), mins=fmt_num(ev["durationMinutes"])),
            M_EV.STR["ms"][dk].format(value=fmt_num(abs(val)), mins=fmt_num(ev["durationMinutes"])),
            M_EV.STR["id"][dk].format(value=fmt_num(abs(val)), mins=fmt_num(ev["durationMinutes"])))

    # -------------------------------------------------- berita pasar ----
    for scope in ("global", "app", "fnb", "logistics"):
        items = [n for n in events["market_news"] if n["scope"] == scope]
        items.sort(key=lambda x: x["id"])
        noun = M_EV.NEWS_NOUN[scope]
        for j, n in enumerate(items):
            if scope == "global":
                if j < 10:
                    text = {l: M_EV.NEWS_PATTERNS["up"][l][j].format(noun=noun[l]) for l in LANGS}
                elif j < 15:
                    gi = j - 10
                    text = {l: M_EV.NEWS_PATTERNS["global_extra"][l][gi].format(noun=noun[l]) for l in LANGS}
                else:
                    di = j - 15
                    text = {l: M_EV.NEWS_PATTERNS["down"][l][di].format(noun=noun[l]) for l in LANGS}
            else:
                if j < 10:
                    text = {l: M_EV.NEWS_PATTERNS["up"][l][j].format(noun=noun[l]) for l in LANGS}
                else:
                    di = (j - 10) % 5
                    text = {l: M_EV.NEWS_PATTERNS["down"][l][di].format(noun=noun[l]) for l in LANGS}
            title = {l: text[l][0].upper() + text[l][1:] for l in LANGS}
            put(n["titleKey"], title["en"], title["ms"], title["id"])

    # ----------------------------------------------------- tutorial ----
    put_all("tu.starter.note",
            M_WORLD.STR["en"]["tu.starter.note"])
    out["ms"]["tu.starter.note"] = M_WORLD.STR["ms"]["tu.starter.note"]
    out["id"]["tu.starter.note"] = M_WORLD.STR["id"]["tu.starter.note"]

    # ----------------------------------------------- semakan & tulis ----
    ref_keys = set(out["en"].keys())
    for lang in ("ms", "id"):
        missing = ref_keys - set(out[lang])
        extra = set(out[lang]) - ref_keys
        if missing or extra:
            raise SystemExit(f"Pariti gagal untuk {lang}: hilang {sorted(missing)[:5]} lebih {sorted(extra)[:5]}")

    # Kunci yang dirujuk data wajib wujud
    referenced = set()
    for fname in C.GAME_DATA.glob("*.json"):
        if fname.name == "balance.json":
            continue
        d = C.load_json(fname)
        TEXT_KEY_FIELDS = {"nameKey", "descKey", "bioKey", "historyKey",
                           "titleKey", "rewardKey", "noteKey"}
        def walk(o):
            if isinstance(o, dict):
                for kk, vv in o.items():
                    if kk in TEXT_KEY_FIELDS and isinstance(vv, str):
                        referenced.add(vv)
                    else:
                        walk(vv)
            elif isinstance(o, list):
                for x in o:
                    walk(x)
        walk(d)
    missing = referenced - ref_keys
    if missing:
        raise SystemExit(f"Kunci dirujuk data tetapi tiada: {sorted(missing)[:10]}")

    # Had panjang
    for lang in LANGS:
        for k, v in out[lang].items():
            lim = key_limit(k)
            if len(v) > lim:
                raise SystemExit(f"Had panjang: {lang} {k} = {len(v)} > {lim}: {v}")

    C.I18N_DIR.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        C.save_json(C.I18N_DIR / f"{lang}.json",
                    {"dataVersion": C.data_version(), "lang": lang, "strings": out[lang]})
        print(f"i18n/{lang}.json: {len(out[lang])} kunci")


if __name__ == "__main__":
    main()
