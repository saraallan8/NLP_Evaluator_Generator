
from app.workflow import run_workflow

question = (
    "What is the purpose of Redis caching in this project?"
)

result = run_workflow(question)

print("\n===== FINAL RESULT =====")
print("Question:", question)
print("Answer:", result["answer"])
print("Approved:", result["approved"])
print("Iterations:", result["iterations"])
print("Feedback:", result["feedback"])
