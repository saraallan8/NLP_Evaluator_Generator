# NLP Evaluator-Generator

An AI-powered question-answering application that uses Retrieval-Augmented Generation (RAG) and an Evaluator-Generator workflow to produce accurate, relevant, and context-grounded answers from your own knowledge sources.

## Overview

The NLP Evaluator-Generator allows users to upload documents, provide website URLs, or retrieve information from Wikipedia. Users can then ask questions about the collected information.

The application retrieves relevant context, generates an answer using a large language model, and evaluates the answer before returning the final result.

## Features

- **Multiple Knowledge Sources:** Upload documents, ingest website URLs, and retrieve Wikipedia content.
- **Audio Transcription:** Transcribe supported audio and video files using OpenAI Whisper.
- **Semantic Search:** Use embeddings and ChromaDB to retrieve relevant information from the knowledge base.
- **RAG Pipeline:** Generate answers grounded in retrieved context.
- **Evaluator-Generator Workflow:** Evaluate answers for accuracy, relevance, completeness, and grounding.
- **Iterative Refinement:** Allow up to four evaluation iterations to improve answers.
- **Redis Caching:** Cache approved results to reduce repeated generation and evaluation.
- **Interactive Web Interface:** Use a Streamlit application to add knowledge sources and ask questions.
- **Source-Aware Responses:** Use retrieved context to help avoid unsupported answers.

## Technologies Used

- Python
- Streamlit
- LangChain
- ChromaDB
- Hugging Face Embeddings
- OpenRouter API
- Large Language Models (LLMs)
- Redis / Memurai
- OpenAI Whisper
- FFmpeg
- Wikipedia API

## Project Structure

```text
NLP_Evaluator_Generator/
│
├── app/
│   ├── cache.py
│   ├── evaluater.py
│   ├── generator.py
│   ├── ingestion.py
│   ├── main.py
│   ├── retrieval.py
│   └── workflow.py
│
├── data/
├── vectorstore/
├── .env
├── .gitignore
├── requirements.txt
└── sample.txt
```

**Note:** The `data/`, `vectorstore/`, `.env`, and virtual environment directories/files should remain local and should not be committed if they contain private data, generated indexes, or secrets.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd NLP_Evaluator_Generator
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's actual GitHub URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Replace the placeholder with your own API key. Never commit your real API key to GitHub.

### 5. Start Redis

Start your local Redis-compatible server. On Windows, this project can use Memurai.

Make sure the server is running before testing caching.

### 6. Configure audio support

For audio and video transcription, install FFmpeg and ensure the `ffmpeg` command is available in your terminal.

OpenAI Whisper may download its speech-recognition model the first time it runs.

### 7. Run the application

From the project root, run:

```bash
streamlit run app/main.py
```

Open the local URL displayed in your terminal.

## How It Works

1. **Ingestion:** The user adds documents, a website URL, a Wikipedia topic, or a supported audio/video file.
2. **Processing:** The application extracts text and splits it into smaller chunks.
3. **Embedding and Storage:** Text chunks are converted into embeddings and stored in ChromaDB.
4. **Retrieval:** The system searches for relevant context based on the user's question.
5. **Generation:** The language model generates an answer using the retrieved context.
6. **Evaluation:** The evaluator checks the generated answer for accuracy, relevance, completeness, and grounding.
7. **Refinement:** If necessary, the workflow repeats generation and evaluation, up to four iterations.
8. **Caching:** Approved results are cached in Redis for reuse.

## Testing

The repository includes standalone Python scripts for testing components such as ingestion, retrieval, generation, evaluation, caching, and workflow behavior.

Run a test script from the project root, for example:

```bash
python test_workflow.py
```

Other available scripts can be run similarly:

```bash
python test_retrieval.py
python test_url_ingestion.py
python test_wikipedia_ingestion.py
python test_audio_ingestion.py
python test_audio_retrieval.py
```

Some tests require a configured API key, a running Redis-compatible server, internet access, or audio dependencies.

## Important Notes

- Answers depend on the quality and relevance of the information in the knowledge base.
- The application may indicate that the provided context does not contain enough information to answer a question.
- Redis caching depends on the question and retrieved context; changes in context can result in a new cache entry.
- Audio transcription quality depends on the recording, language, and selected Whisper model.
- Keep API keys and other sensitive information out of source control.

## Future Improvements

- Add automated unit and integration tests.
- Improve retrieval quality and duplicate-document handling.
- Add conversation history and source citations in the user interface.
- Improve error handling and application logging.
- Deploy the Streamlit application for public access.

## Author

Developed as an NLP project exploring Retrieval-Augmented Generation, semantic search, answer evaluation, and caching.
