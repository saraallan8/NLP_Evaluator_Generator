
from app.ingestion import load_document, split_documents

file_path = "test_audio.mp4"

print("Loading and transcribing audio...")

documents = load_document(file_path)

print("\nTranscription:")
print(documents[0].page_content)

chunks = split_documents(documents)

print("\nNumber of chunks:", len(chunks))
print("Source:", chunks[0].metadata["source"])

print("\nAudio ingestion test completed successfully!")
