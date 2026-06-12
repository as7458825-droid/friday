import os
import uuid

import chromadb
from chromadb.config import Settings

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "memory_db")


def get_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(
        path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False)
    )


def get_or_create_collection(name: str = "workspace"):
    client = get_client()
    return client.get_or_create_collection(name)


def add_to_memory(text: str, metadata: dict | None = None) -> str:
    doc_id = str(uuid.uuid4())
    collection = get_or_create_collection()
    collection.add(
        documents=[text],
        metadatas=[metadata or {}],
        ids=[doc_id],
    )
    return doc_id


def search_memory(query: str, top_k: int = 3) -> list[dict]:
    collection = get_or_create_collection()
    results = collection.query(query_texts=[query], n_results=top_k)
    if not results["documents"] or not results["documents"][0]:
        return []
    return [
        {"text": doc, "metadata": meta, "id": id_}
        for doc, meta, id_ in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["ids"][0],
        )
    ]
