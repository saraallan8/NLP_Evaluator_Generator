from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.retrieval import search

load_dotenv()

def get_generator_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing from .env")

    return ChatOpenAI(
        model="nvidia/nemotron-3.5-lightning:free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )

def generate_answer(question, feedback=None, context=None):
    if context is None:
        documents = search(question)
        context = "\n\n".join(
            document.page_content for document in documents
        )

    if not context.strip():
        return (
            "The required information is not available "
            "in the provided sources."
        )

    prompt = ChatPromptTemplate.from_template("""
You are a Generator LLM in an Evaluator-Generator system.

Answer the question using ONLY the provided context.
Do not invent facts or make unsupported claims.
If the context does not contain the answer, say so.

Previous evaluator feedback:
{feedback}

Context:
{context}

Question:
{question}

Answer:
"""
    )

    chain = prompt | get_generator_llm() | StrOutputParser()

    return chain.invoke({
        "question":question,
        "context":context,
        "feedback":feedback or "No previous feedback.",
    })