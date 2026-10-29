
from app.evaluater import evaluate_answer

question = "What is the maximum number of evaluation iterations?"

context = """
The system must enforce a strict maximum loop count of 4 iterations.
"""

answer = "The maximum number of evaluation iterations is four."

result = evaluate_answer(question, answer, context)

print("Evaluator result:")
print("Approved:", result["approved"])
print("Feedback:", result["feedback"])
