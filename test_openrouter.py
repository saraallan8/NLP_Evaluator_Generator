
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is missing. Check your .env file."
    )

# Connect to OpenRouter
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

# Send a test message
response = llm.invoke(
    "Reply with exactly: OpenRouter connection successful!"
)

print("Connection successful!")
print("Model response:", response.content)
