import re
from pathlib import Path

import pandas as pd
from datasets import load_dataset


OUTPUT_DIR = Path("knowledge_base/dummy_it_helpdesk")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_ITEMS = 30

RELEVANT_KEYWORDS = [
    "printer",
    "mfa",
    "multi-factor",
    "email",
    "password",
    "vpn",
    "wi-fi",
    "wifi",
    "network",
    "internet",
    "software",
    "access",
    "remote desktop",
    "calendar",
    "backup",
    "monitor",
    "phishing",
]


def clean_text(text: str) -> str:
    text = text or ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\S+@\S+", "user@example.com", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:60] or "ticket"


def infer_solution(subject: str, description: str, category: str) -> list[str]:
    text = f"{subject} {description} {category}".lower()

    if "printer" in text:
        return [
            "Pastikan printer dalam keadaan menyala dan terhubung ke jaringan.",
            "Periksa koneksi Wi-Fi atau kabel LAN pada perangkat pengguna.",
            "Pastikan printer yang dipilih sesuai dengan nama printer yang digunakan.",
            "Hapus antrean cetak yang menumpuk pada menu printer queue.",
            "Restart printer dan laptop pengguna.",
            "Jika masih bermasalah, lakukan instalasi ulang driver printer atau hubungi IT Support.",
        ]

    if "mfa" in text or "multi-factor" in text or "authenticator" in text:
        return [
            "Buka portal Microsoft 365 atau halaman login aplikasi terkait.",
            "Login menggunakan akun perusahaan.",
            "Ikuti instruksi pendaftaran MFA yang muncul di layar.",
            "Gunakan aplikasi Microsoft Authenticator atau metode OTP yang tersedia.",
            "Jika mengganti perangkat, lakukan reset MFA melalui administrator IT.",
            "Jika kode tidak diterima atau autentikasi gagal, hubungi IT Support.",
        ]

    if "password" in text:
        return [
            "Pastikan username atau email perusahaan sudah benar.",
            "Gunakan fitur reset password jika tersedia.",
            "Ikuti instruksi verifikasi identitas sesuai kebijakan perusahaan.",
            "Buat password baru sesuai ketentuan keamanan.",
            "Login ulang menggunakan password baru.",
            "Jika akun terkunci, hubungi IT Support atau administrator terkait.",
        ]

    if "vpn" in text:
        return [
            "Pastikan koneksi internet pengguna stabil.",
            "Buka aplikasi VPN yang digunakan perusahaan.",
            "Pastikan username, password, dan MFA sudah benar.",
            "Restart aplikasi VPN dan coba login kembali.",
            "Jika gagal, restart laptop dan jaringan internet.",
            "Jika masalah berlanjut, kirimkan screenshot error ke IT Support.",
        ]

    if "wi-fi" in text or "wifi" in text or "internet" in text or "network" in text:
        return [
            "Pastikan perangkat berada dalam jangkauan jaringan.",
            "Matikan dan nyalakan kembali Wi-Fi pada laptop.",
            "Lupakan jaringan lama, lalu sambungkan kembali menggunakan kredensial yang benar.",
            "Restart laptop dan router jika memungkinkan.",
            "Periksa apakah perangkat lain mengalami masalah yang sama.",
            "Jika masih gagal, hubungi IT Support untuk pengecekan konfigurasi jaringan.",
        ]

    if "email" in text or "sync" in text:
        return [
            "Pastikan koneksi internet stabil.",
            "Buka aplikasi email atau Outlook.",
            "Klik Send/Receive atau lakukan sinkronisasi ulang.",
            "Periksa kapasitas mailbox dan hapus email yang tidak diperlukan.",
            "Restart aplikasi Outlook.",
            "Jika masih bermasalah, buat ulang profil Outlook atau hubungi IT Support.",
        ]

    if "access" in text:
        return [
            "Pastikan nama aplikasi atau folder yang diminta sudah benar.",
            "Pastikan pengguna memiliki persetujuan dari atasan atau pemilik data.",
            "Ajukan request akses melalui kanal resmi perusahaan.",
            "Tim IT akan memverifikasi hak akses pengguna.",
            "Setelah disetujui, akses akan diberikan sesuai kebutuhan.",
            "Jika akses masih gagal, kirimkan screenshot error ke IT Support.",
        ]

    if "phishing" in text:
        return [
            "Jangan klik tautan atau lampiran pada email mencurigakan.",
            "Jangan membalas email dan jangan memasukkan password.",
            "Ambil screenshot atau salin header email jika diperlukan.",
            "Laporkan email tersebut ke tim IT Security atau IT Support.",
            "Hapus email setelah dilaporkan.",
            "Jika terlanjur klik tautan, segera ubah password dan hubungi IT Support.",
        ]

    return [
        "Identifikasi gejala masalah yang dialami pengguna.",
        "Catat pesan error atau kondisi yang muncul.",
        "Restart aplikasi atau perangkat terkait.",
        "Pastikan koneksi jaringan dan akun pengguna berfungsi normal.",
        "Coba ulang proses setelah pengecekan dasar.",
        "Jika masalah belum selesai, eskalasikan ke IT Support dengan detail kendala.",
    ]


def make_kb_content(row: dict) -> str:
    subject = clean_text(row.get("subject", ""))
    description = clean_text(row.get("description", ""))
    category = clean_text(row.get("category", "General"))
    priority = clean_text(row.get("priority", "Medium"))

    steps = infer_solution(subject, description, category)

    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    return f"""Judul: {subject}

Kategori: {category}
Prioritas: {priority}

Deskripsi Masalah:
{description}

Panduan/SOP Penyelesaian:
{steps_text}

Catatan:
Jika panduan ini belum menyelesaikan masalah, pengguna disarankan menghubungi tim IT Support dengan menyertakan screenshot, pesan error, dan kronologi masalah.
"""


def main():
    dataset = load_dataset("Console-AI/IT-helpdesk-synthetic-tickets", split="train")
    df = pd.DataFrame(dataset)

    selected_rows = []

    for _, row in df.iterrows():
        combined_text = f"{row.get('subject', '')} {row.get('description', '')} {row.get('category', '')}".lower()

        if any(keyword in combined_text for keyword in RELEVANT_KEYWORDS):
            selected_rows.append(row.to_dict())

        if len(selected_rows) >= MAX_ITEMS:
            break

    for index, row in enumerate(selected_rows, start=1):
        subject = clean_text(row.get("subject", f"ticket-{index}"))
        filename = f"{index:02d}-{slugify(subject)}.txt"
        file_path = OUTPUT_DIR / filename

        content = make_kb_content(row)

        file_path.write_text(content, encoding="utf-8")

    print(f"Berhasil membuat {len(selected_rows)} file knowledge base di: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()