
from app.generator import generate_answer
from app.evaluater import evaluate_answer
from app.retrieval import search
from app.cache import get_cached_result, set_cached_result

MAX_ITERATIONS = 4

generator_memory = []
evaluater_memory = []


def run_workflow(question):
    documents = search(question)

    context = "\n\n".join(
        document.page_content for document in documents
    )

    if not context.strip():
        return {
            "answer": (
                "The required information is not available "
                "in the provided sources."
            ),
            "approved": False,
            "iterations": 0,
            "feedback": "No relevant knowledge was retrieved.",
        }

    cached_result = get_cached_result(question, context)

    if cached_result is not None:
        print("Cache HIT: Returning cached result.")
        return cached_result

    print("Cache MISS: Running Generator and Evaluator.")

    feedback = None
    answer = ""

    for iteration in range(1, MAX_ITERATIONS + 1):
        answer = generate_answer(
            question,
            feedback=feedback,
            context=context,
        )

        generator_memory.append({
            "question": question,
            "answer": answer,
            "feedback_received": feedback,
        })

        evaluation = evaluate_answer(
            question,
            answer,
            context,
        )

        evaluater_memory.append({
            "question": question,
            "answer": answer,
            "approved": evaluation["approved"],
            "feedback": evaluation["feedback"],
            "iteration": iteration,
        })

        print(f"Iteration: {iteration}")
        print(f"Approved: {evaluation['approved']}")
        print(f"Feedback: {evaluation['feedback']}")

        
        if evaluation["approved"]:
            result = {
                "answer": answer,
                "approved": True,
                "iterations": iteration,
                "feedback": evaluation["feedback"],
            }

            set_cached_result(question, context, result)

            return result

        feedback = evaluation["feedback"]

    return {
        "answer": answer,
        "approved": False,
        "iterations": MAX_ITERATIONS,
        "feedback": (
            "Maximum of four iterations reached. "
            "The latest answer could not be fully validated. "
            f"Last evaluator feedback: {feedback}"
        ),
    }
