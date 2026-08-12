from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv

import os


load_dotenv()


MODEL_NAME = os.getenv(

    "EMBEDDING_MODEL"

)


embedding_model = SentenceTransformer(

    MODEL_NAME

)


def embed(text):

    return embedding_model.encode(text)