from app.services.vector_store import VectorStore


vector_store = VectorStore()

vector_store.get_or_build_index()

print("=" * 60)
print(f"Total chunk terindeks: {vector_store.get_index_size()}")

queries = [
    "Bagaimana cara install printer C3371?",
    "Bagaimana cara install Windows 11?",
    "Bagaimana cara registrasi Microsoft 365?",
    "Kenapa drive tidak muncul saat install Windows?",
]

for query in queries:
    print("=" * 60)
    print(f"Query: {query}")

    results = vector_store.search(query, top_k=3)

    if not results:
        print("Tidak ada hasil retrieval.")
        continue

    for result in results:
        print("-" * 40)
        print(f"Source: {result['source_file']}")
        print(f"Chunk: {result['chunk_index']}")
        print(f"Score: {result['similarity_score']:.4f}")
        print(f"Text: {result['text'][:300]}")