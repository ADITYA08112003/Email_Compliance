from vectorstore.faiss_store import FAISSStore

from utils.file_loader import load_examples

from agents.chunking_agent import chunk_email


store = FAISSStore()


text = load_examples(

    "data/examples.txt"

)


chunks = chunk_email(text)


store.add_documents(chunks)


print("FAISS Index Created Successfully")