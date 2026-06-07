from app.config import settings
from app.services.document_loader import load_and_chunk_knowledge_base
from app.services.embedder import Embedder


chunks = load_and_chunk_knowledge_base(settings.KNOWLEDGE_BASE_PATH)

print("=" * 60)
print(f"Total chunk: {len(chunks)}")

if chunks:
    print("Contoh chunk pertama:")
    print(chunks[0]["source_file"])
    print(chunks[0]["chunk_index"])
    print(chunks[0]["text"][:500])

    embedder = Embedder()

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.embed_texts(texts)

    print("=" * 60)
    print(f"Shape embeddings: {embeddings.shape}")
    print(f"Tipe data: {embeddings.dtype}")