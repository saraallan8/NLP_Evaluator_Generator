from pathlib import Path 
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.ingestion import load_document, split_documents

VECTORSTORE_DIR = Path("vectorstore/chroma.db")

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

def get_vectorstore():

    """open or create persistent chroma database."""

    return Chroma(
        collection_name="external_knowledge",
        embedding_function=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )

def add_file(file_path):
    """load file, spliy it, and save its chunks"""

    documents = load_document(file_path)
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("The uploaded file contains no readble text.")

    vectorstore = get_vectorstore()

    source = chunks[0].metadata["source"]

    existing = vectorstore.get(
        where={"source": source},
        include=["metadatas"],
    )

    if existing["ids"]:
        vectorstore.delete(ids=existing["ids"])

    vectorstore.add_documents(chunks)

    return len(chunks)

def search(question, k=4):
    """Retrieve the most relevant chunks for a question."""

    vectorstore = get_vectorstore()

    return vectorstore.similarity_search(
        question,
        k=k,
    )



