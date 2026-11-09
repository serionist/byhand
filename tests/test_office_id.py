"""Plain Indonesian work text, invented, against the real catalogue. Indonesian has no signs of its own
(`docs/research/2026-11-09-sources-it-tr-vi-id-he-th-fi.md`), so an Indonesian check reads the `any` signs, their
forms under `any` and the one Indonesian form, of `any-assistant-preamble`. A strong or usual sign counts alone, so one
that fires on any of these accuses a person of writing like a machine.

The person's lines are those humanizer-indonesia's D11 and D2 name, which people write too: a colleague's "Tentu,
berikut draf revisinya" to the one who asked, "Semoga membantu", "Jangan ragu untuk menghubungi", and a paper's
"Dengan demikian" or "Sebagai penutup"."""

import pytest

MAIL = [
    "Selamat pagi Bu Rina,\n\nTentu, berikut draf revisinya, Bu:\n\nSaya sudah menambahkan angka kuartal III.\n\n"
    "Salam,\nDimas",
    "Pak Hendra,\n\nTentu, berikut draf revisi kontraknya:\n\nPasal 4 sudah disesuaikan dengan masukan tim legal.",
    "Halo tim,\n\nRapat evaluasi dipindah ke Kamis pukul 14.00 di ruang Melati. Mohon konfirmasi kehadiran.\n\n"
    "Terima kasih,\nSari",
    "Yth. Bapak Agus,\n\nBersama ini kami kirimkan penawaran harga untuk 40 unit laptop. Jangan ragu untuk "
    "menghubungi saya bila ada pertanyaan.\n\nHormat kami,\nPT Sinar Data",
    "Mbak Ayu,\n\nTerlampir notulen rapat kemarin. Semoga membantu!\n\nSalam,\nTika",
    "Dear Pak Budi,\n\nInvoice bulan Oktober belum ada nomor PO-nya. Bisa dicek lagi?\n\nThanks,\nRudi",
]
REPLIES = [
    "Tentu, berikut draf revisinya:",
    "Tentu! Berikut versi terbaru presentasinya, sudah saya ganti grafiknya:",
    "Siap, Pak. Berikut revisi jadwal piket bulan Desember:",
    "Tentu, berikut data penjualan yang Bapak minta:",
]
CHAT = [
    "Oke, nanti sore aku kirim drafnya ya",
    "Tentu, berikut link-nya: https://contoh.co.id/rapat",
    "Semoga membantu, kalau ada yang kurang kabari aja",
    "Siap, makasih ya!",
    "Rapatnya jadi jam 3 kan?",
]
NOTES = [
    "Notulen rapat 12 November\n\n- Anggaran pelatihan disetujui\n- Vendor katering diganti\n- Rapat berikutnya 26 "
    "November",
    "Catatan: server staging mati sejak pukul 09.00, tim infrastruktur sedang menangani.",
]
REPORTS = [
    "Ringkasan\n\nPenjualan kuartal III naik 8% dibanding kuartal II, terutama dari wilayah Jawa Timur. Biaya "
    "logistik masih di atas target.",
    "Penutup\n\nDengan demikian, dapat disimpulkan bahwa program magang menurunkan biaya rekrutmen sebesar 12%.",
    "Sebagai penutup, kami berterima kasih kepada seluruh responden di Surabaya dan Malang.",
]
POSTS = [
    "Minggu lalu tim kami menanam 300 bibit mangrove di pesisir Muara Angke. Terima kasih untuk semua relawan!",
]

KINDS = [
    *((text, "email") for text in MAIL + REPLIES),
    *((text, "message") for text in CHAT),
    *((text, "document") for text in NOTES + REPORTS),
    *((text, "post") for text in POSTS),
]

# What each sign that counts alone exists to catch, inside Indonesian text: a line for the Indonesian form of an `any`
# check, and one for each artefact, which is the same string in every language.
MACHINE = [
    ("any-assistant-preamble", "Tentu, berikut draf revisi email Anda:"),
    ("any-assistant-preamble", "Tentu! Berikut adalah versi revisi dari tulisan Anda, lebih ringkas:"),
    ("any-emoji-markers", "- 🚀 Program pelatihan baru"),
    ("any-unfilled-placeholder", "Pendaftaran: insert_link_here"),
    ("any-chatgpt-citation-markup", "Pendapatan naik. :contentReference[oaicite:0]{index=0}"),
    ("any-chatbot-url-tag", "Sumber: https://contoh.co.id/laporan?utm_source=chatgpt.com"),
]


@pytest.mark.parametrize(("text", "kind"), KINDS)
def test_no_sign_that_counts_alone_fires_on_plain_indonesian_work_text(counted_alone, reads, text, kind):
    fired = [sign.id for sign in counted_alone if reads(sign, kind) and sign.pattern and sign.pattern.search(text)]
    assert fired == []


@pytest.mark.parametrize(("sign", "text"), MACHINE)
def test_the_signs_still_find_what_they_are_for_in_indonesian(catalogue, read_in, sign, text):
    # as an Indonesian check runs it: the forms under id and any, never another language's
    pattern = read_in(catalogue.signs[sign], "id")
    assert pattern is not None
    assert pattern.search(text), sign


def test_every_indonesian_form_of_a_shared_sign_has_a_machine_line(unproven):
    assert unproven(MACHINE, "id") == []


def test_indonesian_has_no_signs_of_its_own(catalogue):
    # so its forms render in a scan file of their own, with no check file beside it
    assert [sign.id for sign in catalogue.signs.values() if sign.language == "id"] == []
