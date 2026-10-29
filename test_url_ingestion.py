
from app.ingestion import load_document, split_documents

url = "https://example.com"

documents = load_document(url)
chunks = split_documents(documents)

print("Documents loaded:", len(documents))
print("Chunks created:", len(chunks))
print("Source:", documents[0].metadata.get("source"))
print("Content preview:", documents[0].page_content[:300])
