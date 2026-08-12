"""
Split large emails/documents into chunks
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_email(email_text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50

    )

    chunks = splitter.split_text(email_text)

    return chunks