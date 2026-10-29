import json 
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
import os 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_evaluater_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing from .env")

    return ChatOpenAI(
        model="nvidia/nemotron-3.5-lightning:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0,
    )

def evaluate_answer(question,answer,context):
    llm = get_evaluater_llm()

    prompt = ChatPromptTemplate.from_template("""

You are an Evaluator LLM.

Evaluate the generated answer using the provided context.

Check:
1. Accuracy
2. Relevance to the question
3. Completeness
4. Consistency with the context
5. Unsupported claims

Return ONLY a valid JSON object with these keys:
- "approved": true or false
- "feedback": a short explanation

Approve only if the answer is supported by the context
and adequately answers the question.

Question:
{question}

Context:
{context}

Generated answer:
{answer}
"""
    )

    chain = prompt | get_evaluater_llm() | StrOutputParser()

    content = chain.invoke({
        "question":question,
        "answer":answer,
        "context":context,
    }).strip() 

    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0].strip()

    try:
        result = json.loads(content)
        approved = result.get("approved")

        if not isinstance(approved, bool):
            raise ValueError("The approved field must be true or false.")

        feedback = result.get("feedback", "")

        return {
            "approved": approved,
            "feedback": str(feedback),
        }

    except (json.JSONDecodeError, ValueError):
        return {
            "approved": False,
            "feedback": (
                "The Evaluator returned an invalid response. "
                "Please generate and evaluate the answer again."
            ),
        }
