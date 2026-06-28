# Chatbot Fullstack

Versi ini dibuat sebagai aplikasi Python tunggal untuk chatbot IT Support berbasis RAG.

## Struktur

- `app/` berisi semua logika Python
- `templates/` berisi tampilan HTML
- `static/` berisi CSS dan JavaScript
- `knowledge_base/` berisi dokumen sumber knowledge base

## Kebutuhan

- Python 3.11 atau lebih baru
- Internet, jika ingin memakai provider Gemini, Groq, atau Hugging Face Router

## Instalasi

1. Masuk ke folder project.

```bash
cd chatbot-fullstack
```

2. Buat virtual environment.

```bash
python3 -m venv .venv
```

3. Aktifkan virtual environment.

```bash
source .venv/bin/activate
```

4. Install dependency.

```bash
python3 -m pip install -r requirements.txt
```

5. Salin file environment.

```bash
cp .env.example .env
```

6. Isi credential di `.env`.

Contoh:

```env
USE_MOCK_LLM=true
LLM_PROVIDER=mock

GEMINI_API_KEY=isi_api_key_gemini
GROQ_API_KEY=isi_api_key_groq
HF_API_KEY=isi_api_key_huggingface
```

## Cara Menjalankan

Jalankan aplikasi dengan Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Lalu buka:

```text
http://127.0.0.1:8000
```

## Provider Model

- `mock`
- `gemini`
- `groq`
- `llama`
- `qwen`

Kalau ingin aplikasi tetap bisa dipakai tanpa credential API, gunakan:

```env
USE_MOCK_LLM=true
LLM_PROVIDER=mock
```

Kalau ingin pakai model asli, ubah `USE_MOCK_LLM=false` dan isi key yang sesuai.

## Catatan

- Index knowledge base dibangun otomatis saat aplikasi membutuhkan pencarian pertama kali.
- File hasil index disimpan di `vector_store/`.
- Karena folder ini standalone, tidak ada project frontend terpisah.
