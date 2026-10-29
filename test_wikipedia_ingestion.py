
from app.ingestion import load_document, split_documents

documents = load_document("wikipedia:Artificial intelligence")
chunks = split_documents(documents)

print("Documents loaded:", len(documents))
print("Chunks created:", len(chunks))

if documents:
    print("Source:", documents[0].metadata.get("source"))
    print("Content preview:", documents[0].page_content[:300])
else:
    print("No Wikipedia documents were returned.")
