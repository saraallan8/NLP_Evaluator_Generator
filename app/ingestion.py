from pathlib import Path
from wikipedia import wikipedia as _wp
from langchain_core.documents import Document
import whisper

_wp.USER_AGENT = "NLPEvaluatorGenerator/1.0 (engsaraallan@gmail.com)"

from langchain_community.document_loaders import(
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    WebBaseLoader,
    WikipediaLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_document(file_path):
    """load a supported document into langchain documents"""

    if file_path.startswith(("wikipedia:")):
        query = file_path.replace("wikipedia:", "", 1).strip()

        loader = WikipediaLoader(
            query=query,
            load_max_docs=2,
            doc_content_chars_max=4000,
        )

        documents = loader.load()

        for document in documents:
            document.metadata["source"] = "wikipedia"

        return documents    

    if file_path.startswith(("http://","https://")):
        loader = WebBaseLoader(web_paths=(file_path,))
        documents = loader.load()

        for document in documents:
            document.metadata["source"] = file_path

        return documents     

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in {".wav",".m4a",".mp4"}:

        model = whisper.load_model("base")
        result = model.transcribe(
        str(path),
        language="en",
        task="transcribe"
     )

        document = Document(
            page_content=result["text"],
            metadata = {"source": path.name}
        )

        return [document]

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))

    elif extension == ".txt" or extension in {
        ".py", ".js", ".html", ".css", ".json", ".sql"
    }:
        loader = TextLoader(str(path), encoding = "utf-8")

    elif extension == ".docx":
        loader = Docx2txtLoader(str(path))

    elif extension == ".pptx":
        loader = UnstructuredPowerPointLoader(str(path))

    else:
        raise ValueError(
            f"Unsupported file {extension}"
        )                

    documents = loader.load()

    for document in documents:
        document.metadata["source"] = path.name

    return documents

def split_documents(documents):
    """split documents into smaller searchable chunks""" 

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 150,
    )   

    return splitter.split_documents(documents)