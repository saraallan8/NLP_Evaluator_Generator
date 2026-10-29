
from app.retrieval import add_file, search

print("Retrieval functions imported successfully!")

chunks_added = add_file("sample.txt")
print(f"Chunks added: {chunks_added}")

results = search(
    "What is the maximum number of evaluation iterations?"
)

for document in results:
    print(document.page_content)
