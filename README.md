# IT Support Chatbot

Repositori ini berisi beberapa versi project chatbot IT Support.

## Struktur Utama

- `chatbot-fullstack/` adalah versi Python tunggal yang direkomendasikan untuk dijalankan.
- `chatbot-backend/` adalah backend lama yang masih disimpan sebagai referensi.
- `chatbot-frontend/` adalah frontend lama yang masih disimpan sebagai referensi.

## Rekomendasi Pemakaian

Jika ingin menjalankan versi yang sudah dirapikan, gunakan folder:

```text
chatbot-fullstack/
```

Versi ini menyatukan UI dan API dalam satu aplikasi Python, dengan konfigurasi credential di file `.env`.

## Cara Menjalankan Versi Fullstack

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

5. Buat file `.env`.

```bash
cp .env.example .env
```

6. Isi credential di `.env`.

Contoh minimal tanpa API key:

```env
USE_MOCK_LLM=true
LLM_PROVIDER=mock
```

Contoh jika ingin memakai model asli:

```env
USE_MOCK_LLM=false
LLM_PROVIDER=gemini
GEMINI_API_KEY=isi_api_key_gemini
GROQ_API_KEY=isi_api_key_groq
HF_API_KEY=isi_api_key_huggingface
```

7. Jalankan aplikasi.

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

8. Buka aplikasi di browser.

```text
http://127.0.0.1:8000
```

## Fitur

- Chatbot RAG untuk IT Support
- UI single app berbasis Python
- Upload dokumen ke knowledge base dari browser
- Rebuild index otomatis setelah upload
- Fallback `mock` jika tidak ingin memakai API model eksternal

## Catatan

- File knowledge base disimpan di `chatbot-fullstack/knowledge_base/`.
- Hasil index lokal disimpan di `chatbot-fullstack/vector_store/`.
- Jangan simpan credential langsung di kode. Gunakan `.env`.

