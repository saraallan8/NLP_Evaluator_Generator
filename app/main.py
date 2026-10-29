import streamlit as st 

from app.retrieval import add_file, search
from app.workflow import run_workflow

st.set_page_config(
    page_title="NLP Evaluator-Genertator",
    page_icon="🤖",
    layout="wide",
)

st.title("NLP Evaluator-Genertator📝")
st.write(
    "Upload documents or ask questions using your existing knowledge base."
)


st.subheader("Upload Your Sources🗂️")

input_type = st.radio(
    "Choose a knowledge source:",
    ["Upload file", "Website URL", "Wikipedia"],
    horizontal=True,
)

if input_type == "Upload file":
    uploaded_file = st.file_uploader(
        "Choose a document or audio file",
        type=[
            "pdf", "txt", "py", "js", "html", "css",
            "json", "sql", "docx", "pptx", "wav", "mp3",
            "m4a", "mp4",
        ],
    )

    if uploaded_file and st.button("Add file to resources"):
        import tempfile
        from pathlib import Path

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            with st.spinner("Processing and indexing your file..."):
                chunks_added = add_file(temp_path)

            st.success(
                f"Successfully added {uploaded_file.name}: "
                f"{chunks_added} chunks."
            )
        except Exception as error:
            st.error(f"Could not process the file: {error}")
        finally:
            Path(temp_path).unlink(missing_ok=True)

elif input_type == "Website URL":
    url = st.text_input("Enter a website URL:")

    if st.button("Add website") and url.strip():
        try:
            with st.spinner("Loading website..."):
                chunks_added = add_file(url.strip())

            st.success(f"Website added: {chunks_added} chunks.")
        except Exception as error:
            st.error(f"Could not process the website: {error}")

elif input_type == "Wikipedia":
    topic = st.text_input("Enter a Wikipedia topic:")

    if st.button("Add Wikipedia topic") and topic.strip():
        try:
            with st.spinner("Loading Wikipedia..."):
                chunks_added = add_file(f"wikipedia:{topic.strip()}")

            st.success(f"Wikipedia topic added: {chunks_added} chunks.")
        except Exception as error:
            st.error(f"Could not process the Wikipedia topic: {error}")


st.subheader("Ask a question")

question = st.text_area(
    "Enter your question",
    placeholder="What would you like to know?",
)

if st.button("Generate Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating and evaluating your answer..."):   
            result = run_workflow(question)

        st.subheader("Answer")
        st.write(result.get("answer","No answer was generated"))

        st.write("Approved:", result.get("approved", False))    
        st.write("Iterations:", result.get("iterations", 0))

        if result.get("feedback"):
            st.write("Feedback:", result["feedback"])

