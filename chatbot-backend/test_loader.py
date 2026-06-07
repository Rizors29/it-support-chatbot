from app.config import settings
from app.services.document_loader import load_document, scan_knowledge_base

files = scan_knowledge_base(settings.KNOWLEDGE_BASE_PATH)

print(f"Jumlah file ditemukan: {len(files)}")

for file in files:
    print("=" * 60)
    print(f"File: {file.name}")

    text = load_document(str(file))

    if text:
        print(f"Jumlah karakter: {len(text)}")
        print(f"Preview: {text[:500]}")
    else:
        print("Gagal membaca file.")