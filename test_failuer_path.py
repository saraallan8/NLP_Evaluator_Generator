
from unittest.mock import patch
from types import SimpleNamespace

from app.workflow import run_workflow

fake_documents = [
    SimpleNamespace(
        page_content="Test context for workflow failure testing."
    )
]

with (
    patch("app.workflow.search", return_value=fake_documents),
    patch(
        "app.workflow.generate_answer",
        return_value="Unverified answer",
    ),
    patch(
        "app.workflow.evaluate_answer",
        return_value={
            "approved": False,
            "feedback": "The answer could not be verified.",
        },
    ),
):
    result = run_workflow(
        "Test four failed evaluation iterations - unique test"
    )

print("\n===== FAILURE PATH TEST =====")
print("Approved:", result["approved"])
print("Iterations:", result["iterations"])
print("Feedback:", result["feedback"])

assert result["approved"] is False
assert result["iterations"] == 4

print("\nSUCCESS: Workflow handled all four failed attempts.")
