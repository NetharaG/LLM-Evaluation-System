import streamlit as st
import requests

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="LLM Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# Title
# -----------------------------------
st.title("🤖 LLM Response Quality Evaluator")
st.write("Evaluate AI-generated responses using RAG and Judge Agents.")

# -----------------------------------
# Question
# -----------------------------------
question = st.text_area(
    "Enter the Question",
    height=120
)

# -----------------------------------
# AI Response
# -----------------------------------
ai_response = st.text_area(
    "Enter the AI Response",
    height=200
)

# -----------------------------------
# Upload PDF
# -----------------------------------
uploaded_file = st.file_uploader(
    "Upload Reference PDF (Optional)",
    type=["pdf"]
)

# -----------------------------------
# Evaluate Button
# -----------------------------------
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

            st.success("✅ Evaluation Completed Successfully!")

            st.header("Evaluation Result")

            # -----------------------------
            # Question
            # -----------------------------
            st.subheader("Question")
            st.write(result["question"])

            # -----------------------------
            # AI Response
            # -----------------------------
            st.subheader("AI Response")
            st.write(result["ai_response"])

            # -----------------------------
            # Reference Answer
            # -----------------------------
            st.subheader("Retrieved Reference Answer")
            st.write(result["reference_answer"])

            # -----------------------------
            # Category
            # -----------------------------
            st.subheader("Category")
            st.write(result["category"])

            st.divider()

            # -----------------------------
            # Judge Agent Scores
            # -----------------------------
            st.header("Judge Agent Evaluation")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Accuracy",
                    result["accuracy"]["score"]
                )

                st.write(result["accuracy"]["reason"])

            with col2:

                st.metric(
                    "Relevance",
                    result["relevance"]["score"]
                )

                st.write(result["relevance"]["reason"])

            with col3:

                st.metric(
                    "Hallucination",
                    result["hallucination"]["score"]
                )

                st.write(result["hallucination"]["reason"])

            st.divider()

            # -----------------------------
            # Raw JSON (Optional)
            # -----------------------------
            with st.expander("View Raw Backend Response"):
                st.json(result)

            # -----------------------------
            # Uploaded PDF
            # -----------------------------
            if uploaded_file is not None:
                st.success(f"Uploaded PDF: {uploaded_file.name}")

        except Exception as e:

            st.error("❌ Backend is not running.")
            st.error(e)