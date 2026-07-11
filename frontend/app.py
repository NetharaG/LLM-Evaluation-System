import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="LLM Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 LLM Response Quality Evaluator")
st.write("Evaluate AI-generated responses using RAG and Judge Agents.")

# -----------------------------
# Question Input
# -----------------------------
question = st.text_area(
    "Enter the Question",
    height=120
)

# -----------------------------
# AI Response Input
# -----------------------------
ai_response = st.text_area(
    "Enter the AI Response",
    height=200
)

# -----------------------------
# Upload PDF (Optional)
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Reference PDF (Optional)",
    type=["pdf"]
)

# -----------------------------
# Evaluate Button
# -----------------------------
if st.button("Evaluate"):

    if question == "" or ai_response == "":
        st.warning("Please enter both Question and AI Response.")
    else:

        payload = {
            "question": question,
            "ai_response": ai_response
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/evaluate",
                json=payload
            )

            result = response.json()

            st.success("Evaluation Completed Successfully!")

            st.subheader("Evaluation Result")

            st.write("### Question")
            st.write(result["question"])

            st.write("### AI Response")
            st.write(result["ai_response"])

            st.write("### Retrieved Reference Answer")
            st.write(result["reference_answer"])

            if uploaded_file is not None:
                st.success(f"Uploaded PDF: {uploaded_file.name}")

        except Exception as e:
            st.error("Backend is not running.")
            st.error(e)