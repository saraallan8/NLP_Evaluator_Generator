
from app.retrieval import add_file, search

file_path = "test_audio.mp4"

print("Adding audio transcript to Chroma...")

chunks_added = add_file(file_path)
print("Chunks added:", chunks_added)

print("\nSearching for information from the recording...")
results = search("What does artificial intelligence help computers understand?")

print("Number of search results:", len(results))

print("\nSearch results:")
for i, document in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(document.page_content)
    print("Source:", document.metadata.get("source"))

print("\nAudio retrieval integration test completed!")
