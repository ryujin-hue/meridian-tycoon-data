#!/usr/bin/env python3
"""Teks entiti: penerangan & sejarah syarikat (templat berslot), bio staf,
bio CEO. Slot diisi oleh generate_i18n.py daripada data sebenar."""

# --------------------------------------------------------------- syarikat --
# Templat desc mengikut sektor x band kategori. Slot: {trait} {city} {year}
DESC_TPL = {
    "app": {
        "starter": {
            "en": "A {trait} two-person shop shipping small apps from {city} since {year}.",
            "ms": "Kedua-dua pengasas menjual app kecil secara {trait} di {city} sejak {year}.",
            "id": "Dua pendiri menjual app kecil secara {trait} di {city} sejak {year}.",
        },
        "midmarket": {
            "en": "A {trait} software house with a few steady clients around {city} since {year}.",
            "ms": "Syarikat perisian {trait} dengan beberapa klien tetap di {city} sejak {year}.",
            "id": "Perusahaan perangkat lunak {trait} dengan beberapa klien tetap di {city} sejak {year}.",
        },
        "rare": {
            "en": "A {trait} product studio whose tools are used across the region, rooted in {city} since {year}.",
            "ms": "Studio produk {trait} yang alatnya dipakai serantau, berakar di {city} sejak {year}.",
            "id": "Studio produk {trait} yang alatnya dipakai se-kawasan, berakar di {city} sejak {year}.",
        },
        "mega": {
            "en": "A {trait} platform giant running nationwide services from {city} since {year}.",
            "ms": "Gergasi platform {trait} yang menjalankan perkhidmatan seluruh negara dari {city} sejak {year}.",
            "id": "Raksasa platform {trait} yang menjalankan layanan se-negara dari {city} sejak {year}.",
        },
    },
    "fnb": {
        "starter": {
            "en": "A {trait} little spot feeding the daily crowd of {city} since {year}.",
            "ms": "Gerai kecil {trait} yang menyuap penduduk {city} setiap hari sejak {year}.",
            "id": "Lapak kecil {trait} yang mengenyangkan warga {city} tiap hari sejak {year}.",
        },
        "midmarket": {
            "en": "A {trait} F&B business with loyal regulars across {city} since {year}.",
            "ms": "Perniagaan makanan {trait} dengan pelanggan tetap di seluruh {city} sejak {year}.",
            "id": "Usaha kuliner {trait} dengan pelanggan setia di seluruh {city} sejak {year}.",
        },
        "rare": {
            "en": "A {trait} prize-winning F&B group running signature outlets in {city} since {year}.",
            "ms": "Grup makanan {trait} pemenang anugerah dengan cawangan tersohor di {city} sejak {year}.",
            "id": "Grup kuliner {trait} peraih penghargaan dengan cabang terkenal di {city} sejak {year}.",
        },
        "mega": {
            "en": "A {trait} nationwide F&B powerhouse with distribution roots in {city} since {year}.",
            "ms": "Kuasa makanan negara yang {trait} dengan pangkalan edaran di {city} sejak {year}.",
            "id": "Raksasa pangan se-negara yang {trait} berbasis distribusi di {city} sejak {year}.",
        },
    },
    "logistics": {
        "starter": {
            "en": "A {trait} courier outfit hauling parcels around {city} since {year}.",
            "ms": "Perkhidmatan kurier {trait} mengangkut bungkusan di sekitar {city} sejak {year}.",
            "id": "Jasa kurir {trait} mengantar paket di sekitar {city} sejak {year}.",
        },
        "midmarket": {
            "en": "A {trait} freight company moving goods between towns since {year}, based in {city}.",
            "ms": "Syarikat kargo {trait} mengangkut barangan antara bandar sejak {year}, berpangkal di {city}.",
            "id": "Perusahaan kargo {trait} mengangkut barang antarkota sejak {year}, berbasis di {city}.",
        },
        "rare": {
            "en": "A {trait} regional carrier with contracts no rival can touch, based in {city} since {year}.",
            "ms": "Pengangkut wilayah {trait} dengan kontrak yang sukar ditandingi, di {city} sejak {year}.",
            "id": "Operator kawasan {trait} dengan kontrak yang tak tertandingi, di {city} sejak {year}.",
        },
        "mega": {
            "en": "A {trait} national logistics backbone anchored at the ports of {city} since {year}.",
            "ms": "Tulang belakang logistik negara yang {trait}, berlabuh di pelabuhan {city} sejak {year}.",
            "id": "Tulang punggung logistik nasional yang {trait}, bersandar di pelabuhan {city} sejak {year}.",
        },
    },
}

TRAITS = {
    "app": {
        "en": ["design-first", "data-driven", "remote-native", "platform-focused",
              "privacy-minded", "open-source friendly", "indie-turned-scale", "product-led"],
        "ms": ["berfokus reka bentuk", "berpandukan data", "sepenuhnya dalam talian",
               "berfokus platform", "hormat privasi", "mesra sumber terbuka",
               "dari indie ke skala besar", "berpandukan produk"],
        "id": ["mengutamakan desain", "berbasis data", "sepenuhnya daring",
               "berfokus platform", "menghormati privasi", "ramah sumber terbuka",
               "dari indie ke skala besar", "berbasis produk"],
    },
    "fnb": {
        "en": ["family-run", "night-market famous", "recipe-driven", "seasonal-menu",
              "chef-led", "community-loved", "street-food classic", "boutique bakery"],
        "ms": ["dikendalikan keluarga", "terkenal di pasar malam", "berpandukan resipi",
               "menu bermusim", "diterajui chef", "kebanggaan komuniti",
               "klasik makanan jalanan", "kedai roti butik"],
        "id": ["dikelola keluarga", "terkenal di pasar malam", "berbasis resep",
               "menu musiman", "dipimpin chef", "kebanggaan komunitas",
               "klasik kuliner jalanan", "toko roti butik"],
    },
    "logistics": {
        "en": ["fleet-backed", "port-adjacent", "cold-chain ready", "last-mile focused",
              "warehouse-first", "rail-linked", "driver-owned", "bonded-storage"],
        "ms": ["sokongan armada", "bersebelahan pelabuhan", "sedia rantaian sejuk",
               "fokus batas akhir", "gudang dahulu", "bersambung rel",
               "milik pemandu", "stor berbond"],
        "id": ["didukung armada", "dekat pelabuhan", "siap rantai dingin",
               "fokus mil terakhir", "gudang dulu", "tersambung rel",
               "milik pengemudi", "gudang berikat"],
    },
}

# Sejarah: templat + slot {origin} {event} {decade} (+ {ceo} {close_year} legacy)
HISTORY_TPL = {
    "en": "Started as {origin}. The {event} made local headlines in the {decade}s.{legacy}",
    "ms": "Mula sebagai {origin}. {event} jadi berita tempatan dekad {decade}an.{legacy}",
    "id": "Dimulai sebagai {origin}. {event} jadi kabar lokal dekade {decade}an.{legacy}",
}
ORIGINS = {
    "en": ["a single market stall", "a rented garage office", "one secondhand lorry",
           "a tiny family kitchen", "a shared co-working desk", "a riverside depot",
           "a night bazaar cart", "a small repair shop"],
    "ms": ["satu gerai pasar", "pejabat garaj sewa", "sebuah lori terpakai",
           "dapur keluarga kecil", "meja ruang kerja kongsi", "depot tepi sungai",
           "kereta pasar malam", "kedai baiki kecil"],
    "id": ["satu lapak pasar", "kantor garasi sewaan", "satu truk bekas",
           "dapur keluarga kecil", "meja ruang kerja bersama", "depot tepi sungai",
           "gerobak pasar malam", "bengkel kecil"],
}
EVENTS = {
    "en": ["first overseas order", "viral customer story", "record sales week",
           "famous loyalty program", "bold rebranding", "industry award",
           "surprise partnership", "legendary sale day"],
    "ms": ["pesanan luar negara pertama", "kisah pelanggan tular", "minggu jualan rekod",
           "program setia masyhur", "penjenamaan semula berani", "anugerah industri",
           "kerjasama mengejut", "hari jualan legenda"],
    "id": ["pesanan luar negeri pertama", "kisah pelanggan viral", "minggu penjualan rekor",
           "program loyalitas terkenal", "rebranding berani", "penghargaan industri",
           "kemitraan mengejutkan", "hari penjualan legendaris"],
}
LEGACY_SUFFIX = {
    "en": " In {close_year}, {ceo} took it over at auction.",
    "ms": " {ceo} ambil alih {close_year} via lelongan.",
    "id": " {ceo} ambil alih {close_year} lewat lelang.",
}

# ------------------------------------------------------------------ staf --
# Bio templat: peranan x jalur bintang (1-2, 3, 4-5) + slot {trait}
STAFF_TPL = {
    "coo": {
        "low": {"en": "Ex-line supervisor who keeps schedules honest. {trait}",
                "ms": "Bekas penyelia litar yang jaga jadual dengan jujur. {trait}",
                "id": "Mantan penyelia lini yang menjaga jadual dengan jujur. {trait}"},
        "mid": {"en": "Runs daily operations like clockwork. {trait}",
                "ms": "Urus operasi harian seperti jam. {trait}",
                "id": "Menjalani operasi harian seperti jam. {trait}"},
        "high": {"en": "Veteran ops director trusted with multi-site rollouts. {trait}",
                 "ms": "Pengarah operasi veteran untuk pelancaran pelbagai lokasi. {trait}",
                 "id": "Direktur operasi veteran untuk peluncuran multilokasi. {trait}"},
    },
    "cfo": {
        "low": {"en": "Junior accountant who never loses a receipt. {trait}",
                "ms": "Akauntan muda yang tidak pernah hilang resit. {trait}",
                "id": "Akuntan muda yang tak pernah kehilangan kuitansi. {trait}"},
        "mid": {"en": "Reads a balance sheet faster than the news. {trait}",
                "ms": "Baca kunci kira-kira lebih pantas daripada berita. {trait}",
                "id": "Membaca neraca lebih cepat daripada berita. {trait}"},
        "high": {"en": "Former bank director who smells bad debt early. {trait}",
                 "ms": "Bekas pengarah bank yang hidu hutang buruk awal. {trait}",
                 "id": "Mantan direktur bank yang mencium utang buruk lebih awal. {trait}"},
    },
    "cmo": {
        "low": {"en": "Social-savvy assistant with a nose for buzz. {trait}",
                "ms": "Pembantu media sosial yang pandai hidu trend. {trait}",
                "id": "Asisten media sosial yang peka tren. {trait}"},
        "mid": {"en": "Turns small budgets into big conversations. {trait}",
                "ms": "Ubah bajet kecil jadi perbualan besar. {trait}",
                "id": "Mengubah anggaran kecil jadi obrolan besar. {trait}"},
        "high": {"en": "Brand architect behind several household names. {trait}",
                 "ms": "Arkitek jenama di sebalik beberapa nama terkenal. {trait}",
                 "id": "Arsitek merek di balik beberapa nama besar. {trait}"},
    },
    "cto": {
        "low": {"en": "Self-taught tinkerer who automates the boring bits. {trait}",
                "ms": "Perkakas belajar sendiri yang automasi kerja membosankan. {trait}",
                "id": "Tukang otodidak yang mengotomatiskan bagian membosankan. {trait}"},
        "mid": {"en": "Ships reliable systems and honest uptime. {trait}",
                "ms": "Bina sistem boleh dipercayai dan masa operasi jujur. {trait}",
                "id": "Membangun sistem andal dan uptime jujur. {trait}"},
        "high": {"en": "Architect of platforms serving millions daily. {trait}",
                 "ms": "Arkitek platform yang berkhidmat kepada jutaan harian. {trait}",
                 "id": "Arsitek platform yang melayani jutaan orang tiap hari. {trait}"},
    },
    "hr": {
        "low": {"en": "Friendly recruiter who remembers every name. {trait}",
                "ms": "Perekrut mesra yang ingat setiap nama. {trait}",
                "id": "Rekruter ramah yang ingat setiap nama. {trait}"},
        "mid": {"en": "Builds onboarding that people actually enjoy. {trait}",
                "ms": "Bina proses induction yang disukai semua. {trait}",
                "id": "Membangun orientasi yang benar-benar disukai. {trait}"},
        "high": {"en": "People director who keeps great teams from drifting. {trait}",
                 "ms": "Pengarah sumber manusia yang halang pasukan hebat terpesong. {trait}",
                 "id": "Direktur SDM yang mencegah tim hebat kehilangan arah. {trait}"},
    },
}
STAFF_TRAITS = {
    "en": ["Loves early mornings.", "Fixes problems quietly.",
           "Never misses a deadline.", "Keeps notebooks full of plans.",
           "Famous for calm under pressure.", "Mentors juniors for free.",
           "Counts coffee as a food group.", "Reads every contract twice."],
    "ms": ["Sayang pagi awal.", "Selesaikan masalah secara senyap.",
           "Tidak pernah terlepas tarikh akhir.", "Buku catatan penuh rancangan.",
           "Terkenal tenang di bawah tekanan.", "Mentori juniors tanpa bayaran.",
           "Kira kopi sebagai makanan asas.", "Baca setiap kontrak dua kali."],
    "id": ["Suka pagi buta.", "Menyelesaikan masalah diam-diam.",
           "Tak pernah melewatkan tenggat.", "Buku catatan penuh rencana.",
           "Terkenal tenang di bawah tekanan.", "Membimbing juniorgratis.",
           "Menghitung kopi sebagai makanan pokok.", "Membaca tiap kontrak dua kali."],
}

# ------------------------------------------------------------------ CEO --
CEO_BIOS = {
    "ceo_rohan_vex": {
        "en": "Bids fast and loud. Rohan treats every auction like a title fight.",
        "ms": "Bida pantas dan kuat. Rohan anggap setiap lelongan seperti pertarungan gelaran.",
        "id": "Menawar cepat dan lantang. Rohan anggap tiap lelang seperti pertarungan gelar.",
    },
    "ceo_danil_wang": {
        "en": "Aggressive on freight and food deals; Danil never blinks first.",
        "ms": "Agresif pada urusan kargo dan makanan; Danil tidak pernah berkelip dulu.",
        "id": "Agresif soal kargo dan kuliner; Danil tak pernah berkedip lebih dulu.",
    },
    "ceo_tariq_halim": {
        "en": "Calculates to the third decimal before raising a finger.",
        "ms": "Mengira hingga titik perpuluhan ketiga sebelum mengangkat jari.",
        "id": "Menghitung sampai tiga desimal sebelum mengangkat jari.",
    },
    "ceo_sasha_kwan": {
        "en": "Quiet, precise, allergic to overpaying. App companies only, mostly.",
        "ms": "Senyap, tepat, alah membayar berlebihan. Syarikat app sahaja, kebanyakkannya.",
        "id": "Tenang, presisi, alergi membayar berlebihan. Perusahaan app saja, kebanyakan.",
    },
    "ceo_maya_rin": {
        "en": "Strikes when rivals hesitate; opportunism is her full-time job.",
        "ms": "Menyerang ketika pesaing teragak-agak; opportunisme kerja sepenuh masanya.",
        "id": "Menyerang saat rival ragu; oportunisme adalah pekerjaan penuhnya.",
    },
    "ceo_laila_suri": {
        "en": "Cautious bidder with deep pockets and shallow appetite.",
        "ms": "Pen bida berhati-hati dengan poket dalam dan selera cetek.",
        "id": "Penawar hati-hati dengan kantong dalam dan selera dangkal.",
    },
    "ceo_victor_nyx": {
        "en": "The Auction Boss. Victor circles legacy giants until the price breaks.",
        "ms": "Boss Lelongan. Victor mengelilingi gergasi legacy sehingga harga pecah.",
        "id": "Bos Lelang. Victor mengepung raksasa legacy sampai harga runtuh.",
    },
}
