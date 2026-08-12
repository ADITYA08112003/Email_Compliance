import json
from pathlib import Path

import faiss
import numpy as np

from embeddings.embedding_model import embed


class FAISSStore:

    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        self.index_path = base_dir / "faiss_index.index"
        self.documents_path = base_dir / "faiss_documents.json"

        self.index = faiss.IndexFlatL2(384)
        self.documents = []
        self._load()

    def _load(self):
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))

        if self.documents_path.exists():
            with open(self.documents_path, "r", encoding="utf-8") as handle:
                self.documents = json.load(handle)

    def save(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))

        with open(self.documents_path, "w", encoding="utf-8") as handle:
            json.dump(self.documents, handle, ensure_ascii=False, indent=2)

    def add_documents(self, docs):
        if not docs:
            return

        vectors = []

        for doc in docs:
            vectors.append(embed(doc))
            self.documents.append(doc)

        self.index.add(np.array(vectors).astype("float32"))
        self.save()

    def search(self, query, k=5):
        if self.index.ntotal == 0 or not self.documents:
            return []

        vector = embed(query)
        distance, index = self.index.search(
            np.array([vector]).astype("float32"),
            min(k, self.index.ntotal)
        )

        results = []

        for d, i in zip(distance[0], index[0]):
            if i != -1 and i < len(self.documents):
                results.append(
                    {
                        "document": self.documents[i],
                        "distance": float(d)
                    }
                )

        return results