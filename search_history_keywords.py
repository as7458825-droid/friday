import os
import chromadb
from chromadb.config import Settings

DB_PATHS = [
    os.path.join(os.getcwd(), "memory_db"),
    os.path.join(os.getcwd(), "data", "memory_db"),
]

KEYWORDS = ["ani", "pagal"]


def search_keywords():
    for db_path in DB_PATHS:
        if not os.path.exists(db_path):
            continue
        print(f"\nSearching in: {db_path}")
        try:
            client = chromadb.PersistentClient(
                path=db_path, settings=Settings(anonymized_telemetry=False)
            )
            collections = client.list_collections()
            for coll_name in [c.name for c in collections]:
                collection = client.get_collection(coll_name)
                results = collection.get()
                docs = results.get("documents", [])
                metas = results.get("metadatas", [])

                for i, doc in enumerate(docs):
                    doc_lower = doc.lower()
                    if any(kw in doc_lower for kw in KEYWORDS):
                        print(f"MATCH FOUND in {coll_name}:")
                        print(f"Text: {doc}")
                        print(f"Metadata: {metas[i]}")
                        print("-" * 20)
        except Exception as e:
            print(f"Error searching {db_path}: {e}")


if __name__ == "__main__":
    search_keywords()
