#!/usr/bin/env python3
"""Kumpulan nama REKAAN Meridian Tycoon (tiada jenama/orang sebenar).

Semua nama ditulis oleh pereka data (bukan dihafal dari dunia sebenar) dan
dijana secara deterministik dengan seed tetap supaya boleh diulang.
Fungsi di sini digunakan oleh generate_companies / generate_staff /
generate_leaderboard DAN generate_i18n supaya nama kekal konsisten.
"""
import itertools
import random

from common import SEED

# ---------------------------------------------------------------- bandar --
# 24 bandar rekaan (gabungan perkataan Melayu yang direka; bukan tempat sebenar)
CITIES = [
    "Bandar Halilintar", "Kota Seri Purnama", "Tanjung Baiduri Mas",
    "Pelabuhan Cendekia", "Lembah Kristal", "Pulau Anggerik Malam",
    "Bandar Cempaka Emas", "Kota Delima Utara", "Tanjung Zamrud Indah",
    "Lembah Baiduri Jaya", "Pulau Seroja Emas", "Bandar Nilam Jaya",
    "Kota Pesisir Cendana", "Tanjung Anggerik Sakti", "Lembah Mutiara Hitam",
    "Pulau Delima Sinar", "Bandar Kenanga Lestari", "Kota Baiduri Sejahtera",
    "Tanjung Purnama Kecil", "Pelabuhan Halilintar Baru", "Kota Zamrud Bahagia",
    "Bandar Seroja Mutiara", "Lembah Nilam Sejuk", "Pulau Cendana Emas",
]


def city_slug(name: str) -> str:
    return "city." + name.lower().replace(" ", "_")


# ------------------------------------------------------------- syarikat --
COMPANY_PREFIX = {
    "app": ["Awan", "Kode", "Piksel", "Nadi", "Vektor", "Sentra", "Laju",
            "Nano", "Arkib", "Ruang", "Suluh", "Terbit", "Gelombang",
            "Digital", "Khabar", "Petir"],
    "fnb": ["Kopi", "Warung", "Dapur", "Roti", "Teh", "Sambal", "Nasi",
            "Kek", "Ais", "Bumbu", "Cendol", "Satay", "Ladang", "Periuk",
            "Saji", "Citarasa"],
    "logistics": ["Kargo", "Lori", "Kapal", "Angkut", "Ekspres", "Rantau",
                  "Muatan", "Feri", "Jalan", "Bungkusan", "Rel", "Dok",
                  "Berat", "Lajur", "Hantar", "Pelayaran"],
}
COMPANY_SUFFIX = {
    "app": ["Cerdas", "Dinamik", "Solusi", "Teknologi", "Sistem", "Inovasi",
            "Prima", "Utama", "Kreatif", "Andalan", "Cepat", "Global",
            "Interaktif", "Ajaib", "Rakan", "Setia"],
    "fnb": ["Sinar", "Nusantara", "Maju", "Bahagia", "Sejahtera", "Harmoni",
            "Ceria", "Lestari", "Purnama", "Anggun", "Bestari", "Gemilang",
            "Abadi", "Ria", "Bakti", "Damai", "Melati", "Kenanga"],
    "logistics": ["Jaya", "Pantas", "Selamat", "Luas", "Samudra", "Perdana",
                  "Bahari", "Megah", "Tepat", "Rancak", "Mutiara", "Pesisir",
                  "Lautan", "Cergas", "Sejati", "Wira"],
}
LEGACY_ROYAL = ["Kumpulan", "Konsortium", "Empayar", "Grup"]
LEGACY_NOUN = {
    "app": ["Kode", "Awan", "Piksel", "Data"],
    "fnb": ["Kopi", "Dapur", "Saji", "Rasa"],
    "logistics": ["Kargo", "Kapal", "Angkut", "Rel"],
}

_COMPANY_SEQ = {}


def _shuffled_combos(sector: str, kind: str) -> list:
    if kind == "regular":
        combos = [f"{p} {s}" for p, s in itertools.product(
            COMPANY_PREFIX[sector], COMPANY_SUFFIX[sector])]
    else:  # legacy
        combos = [f"{r} {n} {s}" for r, n, s in itertools.product(
            LEGACY_ROYAL, LEGACY_NOUN[sector], COMPANY_SUFFIX[sector])]
    idx = C_SECTORS.index(sector) if (C_SECTORS := ["app", "fnb", "logistics"]) else 0
    random.Random(SEED + 91 + idx * 17 + (0 if kind == "regular" else 5)).shuffle(combos)
    return combos


def company_name(sector: str, seq: int, kind: str = "regular") -> str:
    """Nama syarikat deterministik & unik (imbasan turutan tetap)."""
    combos = _shuffled_combos(sector, kind)
    key = (sector, kind)
    _COMPANY_SEQ.setdefault(key, 0)
    name = combos[seq % len(combos)]
    _COMPANY_SEQ[key] += 1
    return name


# ---------------------------------------------------------------- orang --
FIRST = [
    "Adib", "Aina", "Akira", "Alya", "Amanda", "Andre", "Anisa", "Arif",
    "Ayu", "Bianca", "Bryan", "Chandra", "Chen", "Dania", "Dian", "Elena",
    "Emran", "Farah", "Farid", "Gabriel", "Hafiz", "Hana", "Haziq", "Iman",
    "Indra", "Iqbal", "Irma", "Jia", "Kai", "Kavitha", "Kenji", "Kirana",
    "Lea", "Liam", "Lina", "Marcus", "Maya", "Mira", "Nadia", "Naufal",
    "Nik", "Nina", "Omar", "Priya", "Putra", "Rania", "Ravi", "Reza",
    "Rio", "Sari", "Sean", "Sofia", "Tania", "Tara", "Teo", "Wen",
    "Yara", "Yusuf", "Zara",
]
LAST = [
    "Abdullah", "Ahmad", "Chong", "Fernandez", "Goh", "Hamid", "Hassan",
    "Ibrahim", "Iskandar", "Kapoor", "Kassim", "Kim", "Kumar", "Lee", "Lim",
    "Lokman", "Mahmud", "Mansor", "Nakamura", "Ng", "Ong", "Osman",
    "Rahman", "Ramesh", "Rauf", "Santos", "Setiawan", "Sharif", "Syah",
    "Tam", "Tan", "Teh", "Tengku", "Wan", "Wijaya", "Wong", "Yusof",
    "Zainal", "Zulkifli",
]

# Nama CEO ialah rekaan penuh dan TIDAK berasal daripada pool di atas
# (elak pertindihan dengan nama staf/bot).
CEO_NAMES = {
    "ceo_rohan_vex": "Rohan Vex",
    "ceo_maya_rin": "Maya Rin",
    "ceo_tariq_halim": "Tariq Halim",
    "ceo_laila_suri": "Laila Suri",
    "ceo_danil_wang": "Danil Wang",
    "ceo_sasha_kwan": "Sasha Kwan",
    "ceo_victor_nyx": "Victor Nyx",
}


def _person_seq() -> list:
    combos = [f"{f} {l}" for f, l in itertools.product(FIRST, LAST)]
    random.Random(SEED + 41).shuffle(combos)
    return combos


PERSON_SEQ = _person_seq()

# Offset kolam: staf 0-99, bot leaderboard 100-128, kolam nama bot 129-248
STAFF_OFFSET = 0
BOT_OFFSET = 100
BOTPOOL_OFFSET = 129


def person_name(offset: int, index: int) -> str:
    return PERSON_SEQ[(offset + index) % len(PERSON_SEQ)]


# ------------------------------------------------------------------ tag --
COMPANY_TAGS = [
    "fast_growth", "cash_cow", "high_rep", "fixer_upper", "synergy_rich",
    "family_business", "export_power", "local_favourite", "tech_forward",
    "bureaucratic",
]
