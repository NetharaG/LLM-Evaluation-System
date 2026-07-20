import streamlit as st
import requests

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="LLM Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fb;
}

.title{
    text-align:center;
    color:#1f4e79;
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#666666;
    font-size:18px;
    margin-bottom:25px;
}

.section{
    background:white;
    padding:20px;
    border-radius:15px;
    margin-top:10px;
    margin-bottom:15px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.12);
}

.card{
    background:white;
    border-radius:15px;
    padding:18px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.15);
    text-align:center;
}

.green{
    border-left:8px solid #2ecc71;
}

.orange{
    border-left:8px solid orange;
}

.red{
    border-left:8px solid #e74c3c;
}

.metric-title{
    font-size:22px;
    font-weight:bold;
}

.metric-score{
    font-size:40px;
    color:#1f4e79;
    font-weight:bold;
}

.reason{
    color:#444444;
    font-size:16px;
}

.summary-green{
    background:#d4edda;
    color:#155724;
    padding:18px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
}

.summary-yellow{
    background:#fff3cd;
    color:#856404;
    padding:18px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
}

.summary-red{
    background:#f8d7da;
    color:#721c24;
    padding:18px;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div style='
background:linear-gradient(90deg,#1565C0,#42A5F5);
padding:25px;
border-radius:15px;
text-align:center;
margin-bottom:20px;
'>

<h1 style='color:white;margin:0;'>
🤖 LLM Response Quality Evaluator
</h1>

<h4 style='color:white;margin-top:10px;'>
Powered by Retrieval-Augmented Generation (RAG) and LLM Judge Agents
</h4>

</div>
""", unsafe_allow_html=True)
st.divider()

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_color(score):

    if score >= 90:
        return "green"

    elif score >= 70:
        return "orange"

    else:
        return "red"


def get_status(avg):

    if avg >= 90:
        return (
            "summary-green",
            "🟢 Reliable Response"
        )

    elif avg >= 70:
        return (
            "summary-yellow",
            "🟡 Needs Improvement"
        )

    else:
        return (
            "summary-red",
            "🔴 Hallucination Detected"
        )


def show_agent_card(title, icon, score, reason):

    color = get_color(score)

    st.markdown(
        f"""
        <div class="card {color}">
            <div class="metric-title">{icon} {title}</div>
            <div class="metric-score">{score}/100</div>
            <div class="reason">{reason}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(score / 100)
# ============================================
# INPUT SECTION
# ============================================

st.markdown("## 📝 Input Details")

left, right = st.columns([2, 1])

with left:

    question = st.text_area(
        "❓ Enter the Question",
        placeholder="Type the user's question...",
        height=130
    )

    ai_response = st.text_area(
        "🤖 Enter the AI Response",
        placeholder="Paste the AI generated response...",
        height=220
    )

with right:

    uploaded_file = st.file_uploader(
        "📄 Upload Reference PDF (Optional)",
        type=["pdf"]
    )

    st.info(
        """
        **Instructions**

        • Enter a question

        • Enter an AI response

        • Click **Evaluate**

        • Review the Judge Agent results
        """
    )

    if uploaded_file is not None:
        st.success(f"✅ {uploaded_file.name}")

st.divider()

# ============================================
# EVALUATE BUTTON
# ============================================

evaluate = st.button(
    "🚀 Evaluate Response",
    use_container_width=True
)

# ============================================
# BACKEND CALL
# ============================================

if evaluate:

    if question.strip() == "" or ai_response.strip() == "":
        st.warning("⚠ Please enter both Question and AI Response.")

    else:

        payload = {
            "question": question,
            "ai_response": ai_response
        }

        try:

            with st.spinner("🔄 Evaluating using RAG and Judge Agents..."):

                response = requests.post(
                    "http://127.0.0.1:8000/evaluate",
                    json=payload,
                    timeout=120
                )

            if response.status_code != 200:
                st.error("Backend returned an error.")
                st.stop()

            result = response.json()

            st.success("✅ Evaluation Completed Successfully!")

            # ========================================
            # EXTRACT VALUES
            # ========================================

            accuracy_score = result["accuracy"]["score"]
            relevance_score = result["relevance"]["score"]
            hallucination_score = result["hallucination"]["score"]

            accuracy_reason = result["accuracy"]["reason"]
            relevance_reason = result["relevance"]["reason"]
            hallucination_reason = result["hallucination"]["reason"]

            hallucinated_statement = (
                result["hallucination"]
                .get("hallucinated_statement",
                     "No hallucinated information detected.")
            )

            average_score = round(
                (
                    accuracy_score
                    + relevance_score
                    + hallucination_score
                ) / 3,
                2
            )

            css_class, overall_status = get_status(average_score)
            # ========================================
            # INPUT SUMMARY
            # ========================================

            st.divider()
            st.header("📋 Evaluation Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ❓ Question")
                st.info(result["question"])

                st.markdown("### 🤖 AI Response")
                st.success(result["ai_response"])

            with col2:
                st.markdown("### 📚 Retrieved Reference")
                st.warning(result["reference_answer"])

                st.markdown("### 🏷 Category")
                st.write(result["category"])

            st.divider()

            # ========================================
            # JUDGE AGENTS
            # ========================================

            st.header("📊 Judge Agent Evaluation")

            c1, c2, c3 = st.columns(3)

            with c1:
                show_agent_card(
                    "Accuracy Agent",
                    "✅",
                    accuracy_score,
                    accuracy_reason
                )

            with c2:
                show_agent_card(
                    "Relevance Agent",
                    "🎯",
                    relevance_score,
                    relevance_reason
                )

            with c3:
                show_agent_card(
                    "Hallucination Agent",
                    "🚨",
                    hallucination_score,
                    hallucination_reason
                )

            st.divider()

            # ========================================
            # SCORE DASHBOARD
            # ========================================

            st.header("📈 Performance Dashboard")

            p1, p2, p3 = st.columns(3)

            with p1:
                st.metric("Accuracy", f"{accuracy_score}/100")

            with p2:
                st.metric("Relevance", f"{relevance_score}/100")

            with p3:
                st.metric("Hallucination", f"{hallucination_score}/100")

            st.metric(
                "⭐ Overall Average",
                f"{average_score}/100"
            )

            st.divider()

            # ========================================
            # OVERALL STATUS
            # ========================================

            st.header("📝 Overall Evaluation")

            st.markdown(
                f"""
                <div class="{css_class}">
                    {overall_status}
                    <br><br>
                    Overall Score : <b>{average_score}/100</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            # ========================================
            # HALLUCINATION SECTION
            # ========================================

            st.header("🚨 Hallucination Detection")
            if hallucination_score >= 90:
                st.success("✅ No Hallucinated Statement Detected.")
            else:
                st.error("⚠ Hallucination Detected")
                st.write("### Unsupported Statement")
                st.warning(hallucinated_statement)

            st.divider()

            # ========================================
            # VALIDATION STATUS
            # ========================================

            st.header("✔ Validation Status")

            v1, v2, v3 = st.columns(3)

            with v1:

                if accuracy_score >= 90:
                    st.success("Accuracy Passed")
                else:
                    st.warning("Accuracy Needs Improvement")

            with v2:

                if relevance_score >= 90:
                    st.success("Relevance Passed")
                else:
                    st.warning("Relevance Needs Improvement")

            with v3:

                if hallucination_score >= 90:
                    st.success("Hallucination Passed")
                else:
                    st.error("Hallucination Detected")

            st.divider()

            # ========================================
            # RAW JSON
            # ========================================

            with st.expander("📂 View Backend JSON"):

                st.json(result)

        except Exception as e:

            st.error("❌ Unable to connect to backend.")

            st.exception(e)