import asyncio

from app.services.rag_service import RAGService


async def main():
    rag = RAGService()

    queries = [
        "Bagaimana cara install printer C3371?",
        "Bagaimana cara registrasi Microsoft 365?",
        "Kenapa drive tidak muncul saat install Windows?",
        "Bagaimana cara mengurus cuti karyawan?",
    ]

    for query in queries:
        print("=" * 80)
        print(f"Query: {query}")

        response = await rag.process_query(query)

        print(f"Kategori: {response['category']}")
        print(f"Fallback: {response['is_fallback']}")
        print(f"Score: {response['similarity_score']:.4f}")
        print(f"Sumber: {response['sources']}")
        print("Jawaban:")
        print(response["answer"])


if __name__ == "__main__":
    asyncio.run(main())