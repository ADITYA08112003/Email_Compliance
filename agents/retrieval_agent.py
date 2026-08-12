"""
Retrieve similar compliance examples
using FAISS
"""

from vectorstore.faiss_store import FAISSStore

store = FAISSStore()


def retrieve_examples(email):

    results = store.search(

        email,

        k=5

    )

    return results