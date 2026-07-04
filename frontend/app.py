import streamlit as st
import requests
# Page configuration
st.set_page_config(
    page_title="LLM Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 LLM Response Quality Evaluator")

st.write("Evaluate AI-generated responses using multiple judge agents.")

# Question
question = st.text_area(
    "Enter the Question",
    height=120
)

# AI Response
ai_response = st.text_area(
    "Enter the AI Response",
    height=200
)

# Reference Answer
reference_answer = st.text_area(
    "Reference Answer (Optional)",
    height=150
)

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload Reference PDF (Optional)",
    type=["pdf"]
)

# Evaluate Button
if st.button("Evaluate"):

    payload = {
        "question": question,
        "ai_response": ai_response,
        "reference_answer": reference_answer
    }

    response = requests.post(
        "http://127.0.0.1:8000/evaluate",
        json=payload
    )

    result = response.json()

    st.success("Evaluation Request Sent Successfully!")

    st.write("### Backend Response")

    st.json(result)

    if uploaded_file:
        st.write("Uploaded File:", uploaded_file.name)
    else:
        st.write("No PDF uploaded.")