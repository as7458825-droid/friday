import os
import chromadb
from chromadb.config import Settings

CHROMA_DIR = os.path.join(os.getcwd(), "memory_db")


def recover_history():
    print(f"Connecting to ChromaDB at {CHROMA_DIR}...")
    try:
        client = chromadb.PersistentClient(
            path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False)
        )
        collections = client.list_collections()
        print(f"Found collections: {[c.name for c in collections]}")

        for coll_name in [c.name for c in collections]:
            print(f"\n--- History from collection: {coll_name} ---")
            collection = client.get_collection(coll_name)
            results = collection.get()

            docs = results.get("documents", [])
            metas = results.get("metadatas", [])
            ids = results.get("ids", [])

            if not docs:
                print("No records found.")
                continue

            for i in range(len(docs)):
                print(f"ID: {ids[i]}")
                print(f"Metadata: {metas[i]}")
                print(f"Text: {docs[i]}")
                print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    recover_history()
