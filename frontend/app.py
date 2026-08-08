import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from reports.pdf_report import generate_pdf
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
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
            completeness_score = result["completeness"]["score"]
            completeness_reason = result["completeness"]["reason"]
            missing_points = result["completeness"]["missing_points"]
            overall_score = result["verdict"]["overall_score"]
            overall_verdict = result["verdict"]["verdict"]
            overall_summary = result["verdict"]["summary"]

            hallucinated_statement = (
                result["hallucination"]
                .get("hallucinated_statement",
                     "No hallucinated information detected.")
            )

            average_score = overall_score

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

            c1, c2, c3, c4 = st.columns(4)

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

            with c4:
                show_agent_card(
                    "Completeness Agent",
                    "📄",
                    completeness_score,
                    completeness_reason
                )
            st.divider()

            # ========================================
            # SCORE DASHBOARD
            # ========================================

            st.header("📈 Performance Dashboard")
            p1, p2, p3, p4 = st.columns(4)

            with p1:
                st.metric("Accuracy", f"{accuracy_score}/100")

            with p2:
                st.metric("Relevance", f"{relevance_score}/100")

            with p3:
                st.metric("Hallucination", f"{hallucination_score}/100")

            with p4:
                st.metric("Completeness", f"{completeness_score}/100")

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
                    Verdict : <b>{overall_verdict}</b>
                    <br><br>
                    Overall Score : <b>{overall_score}/100</b>
                    <br><br>
                    {overall_summary}
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

            st.header("📄 Completeness Analysis")
            st.info(completeness_reason)
            if missing_points.strip().lower() != "none":
                st.warning("Missing Points")
                st.write(missing_points)
            else:
                st.success("No important information is missing.")

            # ========================================
            # VALIDATION STATUS
            # ========================================

            st.header("✔ Validation Status")

            v1, v2, v3, v4 = st.columns(4)

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

            with v4:
                if completeness_score >= 90:
                    st.success("Completeness Passed")
                else:
                    st.warning("Completeness Needs Improvement")

            st.divider()

            # ========================================
            # RAW JSON
            # ========================================

            with st.expander("📂 View Backend JSON"):

                st.json(result)

        except Exception as e:

            st.error("❌ Unable to connect to backend.")

            st.exception(e)
# ============================================
# BATCH EVALUATION MODULE
# ============================================

st.divider()
st.header("📂 Batch Evaluation Module")

batch_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"],
    key="batch_csv"
)

batch_button = st.button(
    "🚀 Evaluate Batch",
    use_container_width=True
)

# ============================================
# READ CSV
# ============================================

if batch_button:

    if batch_file is None:
        st.warning("⚠ Please upload a CSV file.")

    else:

        try:

            # Read CSV
            df = pd.read_csv(batch_file)

            st.success("✅ CSV Uploaded Successfully")

            st.subheader("Preview")

            st.dataframe(df, use_container_width=True)

            # Validate columns
            required_columns = ["question", "ai_response"]

            if not all(col in df.columns for col in required_columns):

                st.error("CSV must contain columns: question, ai_response")
                st.stop()

            # ============================================
            # SEND TO BACKEND
            # ============================================

            payload = {
                "evaluations": []
            }

            for _, row in df.iterrows():

                payload["evaluations"].append({
                    "question": row["question"],
                    "ai_response": row["ai_response"]
                })

            with st.spinner("Evaluating all responses..."):

                response = requests.post(
                    "http://127.0.0.1:8000/batch_evaluate",
                    json=payload,
                    timeout=600
                )

            if response.status_code != 200:

                st.error("Batch evaluation failed.")
                st.stop()

            batch_result = response.json()

            st.success("✅ Batch Evaluation Completed Successfully!")

            # ============================================
            # DISPLAY RESULTS
            #  ============================================
            results = []
            for item in batch_result["results"]:
                results.append({
                    "Question": item["question"],
                    "Accuracy": item["accuracy"]["score"],
                    "Relevance": item["relevance"]["score"],
                    "Hallucination": item["hallucination"]["score"],
                    "Completeness": item["completeness"]["score"],
                    "Overall Score": item["verdict"]["overall_score"],
                    "Verdict": item["verdict"]["verdict"]
                 })
            result_df = pd.DataFrame(results)
            st.subheader("📊 Batch Evaluation Results")
            st.dataframe(result_df, use_container_width=True)

            
            # ======================================================
            # DASHBOARD SUMMARY
            # ======================================================
            st.divider()
            st.markdown("## 📊 Evaluation Dashboard")
            
            # ----------------------------
            # Calculate Statistics
            # ----------------------------
            
            total_evaluations = len(result_df)
            
            pass_count = len(result_df[result_df["Verdict"] == "Pass"])
            
            needs_improvement_count = len(
                result_df[result_df["Verdict"] == "Needs Improvement"]
            )
            
            fail_count = len(result_df[result_df["Verdict"] == "Fail"])
            
            avg_accuracy = round(result_df["Accuracy"].mean(), 2)
            avg_relevance = round(result_df["Relevance"].mean(), 2)
            avg_hallucination = round(result_df["Hallucination"].mean(), 2)
            avg_completeness = round(result_df["Completeness"].mean(), 2)
            avg_overall = round(result_df["Overall Score"].mean(), 2)
            
            # ----------------------------
            # First Row
            # ----------------------------
            
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                st.metric(
                    label="📄 Total Evaluations",
                    value=total_evaluations
                )
            
            with c2:
                st.metric(
                    label="✅ Pass",
                    value=pass_count
                )
            
            with c3:
                st.metric(
                    label="🟡 Needs Improvement",
                    value=needs_improvement_count
                )
            
            with c4:
                st.metric(
                    label="❌ Fail",
                    value=fail_count
                )
            
            st.divider()
            
            # ----------------------------
            # Second Row
            # ----------------------------
            
            c5, c6, c7, c8, c9 = st.columns(5)
            
            with c5:
                st.metric(
                    "Accuracy",
                    f"{avg_accuracy}"
                )
            
            with c6:
                st.metric(
                    "Relevance",
                    f"{avg_relevance}"
                )
            
            with c7:
                st.metric(
                    "Hallucination",
                    f"{avg_hallucination}"
                )
            
            with c8:
                st.metric(
                    "Completeness",
                    f"{avg_completeness}"
                )
            
            with c9:
                st.metric(
                    "Overall Score",
                    f"{avg_overall}"
                )
            
            st.divider()
            # ======================================================
            # DASHBOARD CHARTS
            # ======================================================
            
            st.markdown("## 📈 Dashboard Visualizations")
            
            # ----------------------------
            # Data Preparation
            # ----------------------------
            
            verdict_counts = (
                result_df["Verdict"]
                .value_counts()
                .reset_index()
            )
            
            verdict_counts.columns = ["Verdict", "Count"]
            
            score_df = pd.DataFrame({
                "Agent": [
                    "Accuracy",
                    "Relevance",
                    "Hallucination",
                    "Completeness"
                ],
                "Average Score": [
                    avg_accuracy,
                    avg_relevance,
                    avg_hallucination,
                    avg_completeness
                ]
            })
            
            hallucination_df = pd.DataFrame({
                "Status": [
                    "No Hallucination",
                    "Hallucination Found"
                ],
                "Count": [
                    len(result_df[result_df["Hallucination"] >= 90]),
                    len(result_df[result_df["Hallucination"] < 90])
                ]
            })
            
            trend_df = result_df.copy()
            trend_df["Evaluation"] = range(1, len(trend_df)+1)
            
            # ======================================================
            # FIRST ROW
            # ======================================================
            
            left, right = st.columns(2)
            
            # ---------------------------------------------
            # Verdict Distribution
            # ---------------------------------------------
            
            with left:
            
                fig1 = px.bar(
                    verdict_counts,
                    x="Verdict",
                    y="Count",
                    color="Verdict",
                    text="Count",
                    title="📊 Verdict Distribution",
                    color_discrete_map={
                        "Pass": "#2ecc71",
                        "Needs Improvement": "#f39c12",
                        "Fail": "#e74c3c"
                    }
                )
            
                fig1.update_layout(
                    template="plotly_white",
                    height=420,
                    title_x=0.25
                )
                fig1.write_image("reports/verdict_distribution.png")
                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )
            
            # ---------------------------------------------
            # Average Agent Scores
            # ---------------------------------------------
            
            with right:
            
                fig2 = px.bar(
                    score_df,
                    x="Agent",
                    y="Average Score",
                    color="Agent",
                    text="Average Score",
                    title="📈 Average Agent Scores"
                )
            
                fig2.update_layout(
                    template="plotly_white",
                    yaxis_range=[0,100],
                    height=420,
                    title_x=0.20
                )
                fig2.write_image("reports/average_scores.png")
                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )
            
            # ======================================================
            # SECOND ROW
            # ======================================================
            
            left2, right2 = st.columns(2)
            
            # ---------------------------------------------
            # Hallucination Frequency
            # ---------------------------------------------
            
            with left2:
            
                fig3 = px.pie(
                    hallucination_df,
                    names="Status",
                    values="Count",
                    hole=0.55,
                    title="🚨 Hallucination Frequency",
                    color="Status",
                    color_discrete_map={
                        "No Hallucination":"#2ecc71",
                        "Hallucination Found":"#e74c3c"
                    }
                )
            
                fig3.update_layout(
                    height=420
                )
                fig3.write_image("reports/hallucination.png")
                st.plotly_chart(
                    fig3,
                    use_container_width=True
                )
            
            # ---------------------------------------------
            # Quality Trend
            # ---------------------------------------------
            
            with right2:
            
                fig4 = px.line(
                    trend_df,
                    x="Evaluation",
                    y="Overall Score",
                    markers=True,
                    title="📈 Quality Trend"
                )
            
                fig4.update_traces(
                    line_width=4
                )
            
                fig4.update_layout(
                    template="plotly_white",
                    yaxis_range=[0,100],
                    height=420
                )
                fig4.write_image("reports/quality_trend.png")
                st.plotly_chart(
                    fig4,
                    use_container_width=True
                )
            
            st.divider()

            # =====================================================
            # PDF REPORT EXPORT
            # =====================================================
                                                                
            st.divider()
            st.header("📄 Export Evaluation Report")
                                                                
            pdf_file = generate_pdf(result_df)
                                                                
            with open(pdf_file, "rb") as pdf:
                                                                
                st.download_button(
                label="📥 Download PDF Report",
                data=pdf,
                file_name="LLM_Evaluation_Report.pdf",
                mime="application/pdf",
                use_container_width=True
                )                                                                                           
            
            # ======================================================
            # BATCH INSIGHTS
            # ======================================================
            
            st.markdown("## 📌 Batch Insights")
            
            best_response = result_df.loc[result_df["Overall Score"].idxmax()]
            worst_response = result_df.loc[result_df["Overall Score"].idxmin()]
            
            left, right = st.columns(2)
            
            # ======================================================
            # BEST RESPONSE
            # ======================================================
            
            with left:
            
                st.success("🏆 Best Performing Response")
            
                st.write("**Question**")
                st.info(best_response["Question"])
            
                st.metric(
                    "Overall Score",
                    best_response["Overall Score"]
                )
            
                st.write("**Verdict**")
                st.success(best_response["Verdict"])
            
            # ======================================================
            # WORST RESPONSE
            # ======================================================
            
            with right:
            
                st.error("⚠ Lowest Performing Response")
            
                st.write("**Question**")
                st.warning(worst_response["Question"])
            
                st.metric(
                    "Overall Score",
                    worst_response["Overall Score"]
                )
            
                st.write("**Verdict**")
                st.warning(worst_response["Verdict"])
            
            st.divider()
            
            # ======================================================
            # SUMMARY
            # ======================================================
            
            st.markdown("## 📋 Batch Summary")
            
            summary = f"""
            
            Total Evaluations : {total_evaluations}
            
            Passed : {pass_count}
            
            Needs Improvement : {needs_improvement_count}
            
            Failed : {fail_count}
            
            Average Accuracy : {avg_accuracy}
            
            Average Relevance : {avg_relevance}
            
            Average Hallucination : {avg_hallucination}
            
            Average Completeness : {avg_completeness}
            
            Overall Average Score : {avg_overall}
            
            """
            
            st.info(summary)
            
            # ======================================================
            # RECOMMENDATIONS
            # ======================================================
            
            st.markdown("## 💡 Improvement Recommendations")
            
            recommendations = []
            
            if avg_accuracy < 90:
                recommendations.append(
                    "• Improve factual correctness of AI responses."
                )
            
            if avg_relevance < 90:
                recommendations.append(
                    "• Improve relevance to user questions."
                )
            
            if avg_hallucination < 90:
                recommendations.append(
                    "• Reduce hallucinated statements."
                )
            
            if avg_completeness < 90:
                recommendations.append(
                    "• Improve completeness of answers."
                )
            
            if len(recommendations) == 0:
            
                st.success(
                    "🎉 Excellent! All evaluation dimensions are performing well."
                )
            
            else:
            
                for rec in recommendations:
            
                    st.warning(rec)
            
            st.divider()
            
        except Exception as e:

            st.error("Unable to read CSV.")
            st.exception(e)