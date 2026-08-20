# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Table,
#     TableStyle,
#     Paragraph,
#     Spacer,
#     PageBreak,
#     Image,
#     KeepTogether
# )
# import matplotlib.pyplot as plt
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.enums import TA_CENTER
# from reportlab.lib.units import inch

# import os
# from datetime import datetime

# from rag.pdf_reference import BASE_DIR

# from rag.pdf_reference import BASE_DIR


# # =========================================================
# # GENERATE PDF
# # =========================================================

# def generate_pdf(result_df):

#     # -----------------------------------------------------
#     # File locations
#     # -----------------------------------------------------

#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#     pdf_file = os.path.join(
#         BASE_DIR,
#         "LLM_Evaluation_Report.pdf"
#     )

#     # -----------------------------------------------------
#     # PDF document
#     # -----------------------------------------------------

#     doc = SimpleDocTemplate(
#         pdf_file,
#         pagesize=A4,
#         rightMargin=35,
#         leftMargin=35,
#         topMargin=35,
#         bottomMargin=35
#     )

#     # -----------------------------------------------------
#     # Styles
#     # -----------------------------------------------------

#     styles = getSampleStyleSheet()

#     title_style = ParagraphStyle(
#         "CustomTitle",
#         parent=styles["Title"],
#         fontSize=24,
#         leading=30,
#         alignment=TA_CENTER,
#         textColor=colors.HexColor("#17365D"),
#         spaceAfter=20
#     )

#     heading_style = ParagraphStyle(
#         "CustomHeading",
#         parent=styles["Heading1"],
#         fontSize=18,
#         leading=22,
#         textColor=colors.HexColor("#17365D"),
#         spaceBefore=8,
#         spaceAfter=12
#     )

#     normal_style = ParagraphStyle(
#         "CustomNormal",
#         parent=styles["Normal"],
#         fontSize=10,
#         leading=15,
#         spaceAfter=8
#     )

#     small_style = ParagraphStyle(
#         "Small",
#         parent=styles["Normal"],
#         fontSize=8,
#         leading=10
#     )

#     story = []

#     # =====================================================
#     # CALCULATE SUMMARY
#     # =====================================================

#     total = len(result_df)

#     passed = len(
#         result_df[result_df["Verdict"] == "Pass"]
#     )

#     needs = len(
#         result_df[
#             result_df["Verdict"] == "Needs Improvement"
#         ]
#     )

#     failed = len(
#         result_df[result_df["Verdict"] == "Fail"]
#     )

#     avg_accuracy = round(
#         result_df["Accuracy"].mean(), 2
#     )

#     avg_relevance = round(
#         result_df["Relevance"].mean(), 2
#     )

#     avg_hallucination = round(
#         result_df["Hallucination"].mean(), 2
#     )

#     avg_completeness = round(
#         result_df["Completeness"].mean(), 2
#     )

#     avg_overall = round(
#         result_df["Overall Score"].mean(), 2
#     )

#     # =====================================================
#     # COVER PAGE
#     # =====================================================

#     story.append(Spacer(1, 0.7 * inch))

#     story.append(
#         Paragraph(
#             "LLM RESPONSE QUALITY<br/>"
#             "EVALUATION REPORT",
#             title_style
#         )
#     )

#     story.append(
#         Spacer(1, 0.3 * inch)
#     )

#     cover_data = [
#         ["Project", "LLM Response Quality Evaluation System"],
#         ["Evaluation Mode", "Batch Evaluation"],
#         ["Total Responses", str(total)],
#         [
#             "Generated On",
#             datetime.now().strftime(
#                 "%d-%m-%Y %H:%M:%S"
#             )
#         ],
#     ]

#     cover_table = Table(
#         cover_data,
#         colWidths=[1.7 * inch, 4.7 * inch]
#     )

#     cover_table.setStyle(
#         TableStyle([
#             (
#                 "BACKGROUND",
#                 (0, 0),
#                 (0, -1),
#                 colors.HexColor("#D9EAF7")
#             ),
#             (
#                 "FONTNAME",
#                 (0, 0),
#                 (0, -1),
#                 "Helvetica-Bold"
#             ),
#             (
#                 "GRID",
#                 (0, 0),
#                 (-1, -1),
#                 0.5,
#                 colors.grey
#             ),
#             (
#                 "VALIGN",
#                 (0, 0),
#                 (-1, -1),
#                 "MIDDLE"
#             ),
#             (
#                 "TOPPADDING",
#                 (0, 0),
#                 (-1, -1),
#                 10
#             ),
#             (
#                 "BOTTOMPADDING",
#                 (0, 0),
#                 (-1, -1),
#                 10
#             ),
#         ])
#     )

#     story.append(cover_table)

#     story.append(
#         Spacer(1, 0.6 * inch)
#     )

#     story.append(
#         Paragraph(
#             "This report presents the automated evaluation "
#             "of AI-generated responses using Accuracy, "
#             "Relevance, Hallucination and Completeness "
#             "evaluation metrics.",
#             normal_style
#         )
#     )

#     story.append(PageBreak())

#     # =====================================================
#     # EXECUTIVE SUMMARY
#     # =====================================================

#     story.append(
#         Paragraph(
#             "Executive Summary",
#             heading_style
#         )
#     )

#     summary_data = [
#         ["Metric", "Value"],
#         ["Total Evaluations", total],
#         ["Passed", passed],
#         ["Needs Improvement", needs],
#         ["Failed", failed],
#         ["Average Accuracy", avg_accuracy],
#         ["Average Relevance", avg_relevance],
#         ["Average Hallucination", avg_hallucination],
#         ["Average Completeness", avg_completeness],
#         ["Average Overall Score", avg_overall],
#     ]

#     summary_table = Table(
#         summary_data,
#         colWidths=[3.8 * inch, 2.0 * inch]
#     )

#     summary_table.setStyle(
#         TableStyle([
#             (
#                 "BACKGROUND",
#                 (0, 0),
#                 (-1, 0),
#                 colors.HexColor("#17365D")
#             ),
#             (
#                 "TEXTCOLOR",
#                 (0, 0),
#                 (-1, 0),
#                 colors.white
#             ),
#             (
#                 "FONTNAME",
#                 (0, 0),
#                 (-1, 0),
#                 "Helvetica-Bold"
#             ),
#             (
#                 "GRID",
#                 (0, 0),
#                 (-1, -1),
#                 0.5,
#                 colors.grey
#             ),
#             (
#                 "BACKGROUND",
#                 (0, 1),
#                 (-1, -1),
#                 colors.HexColor("#F4F7FA")
#             ),
#             (
#                 "ALIGN",
#                 (1, 1),
#                 (1, -1),
#                 "CENTER"
#             ),
#             (
#                 "TOPPADDING",
#                 (0, 0),
#                 (-1, -1),
#                 7
#             ),
#             (
#                 "BOTTOMPADDING",
#                 (0, 0),
#                 (-1, -1),
#                 7
#             ),
#         ])
#     )

#     story.append(summary_table)

#     story.append(
#         Spacer(1, 0.3 * inch)
#     )

#     # Short summary paragraph

#     story.append(
#         Paragraph(
#             f"""
#             The system evaluated <b>{total}</b> AI-generated
#             responses. A total of <b>{passed}</b> responses
#             passed the evaluation, <b>{needs}</b> required
#             improvement and <b>{failed}</b> failed.
#             The average overall evaluation score was
#             <b>{avg_overall}</b>.
#             """,
#             normal_style
#         )
#     )

#     story.append(PageBreak())
#     # =====================================================
#     # GENERATE DASHBOARD CHARTS
#     # =====================================================

#     # 1. Verdict Distribution
#     verdict_counts = result_df["Verdict"].value_counts()

#     plt.figure(figsize=(8, 4))
#     verdict_counts.plot(kind="bar")
#     plt.title("Verdict Distribution")
#     plt.xlabel("Verdict")
#     plt.ylabel("Number of Responses")
#     plt.tight_layout()
#     plt.savefig(os.path.join(BASE_DIR, "verdict_distribution.png"), dpi=150)
#     plt.close()

#     # 2. Average Agent Scores
#     average_scores = [
#         result_df["Accuracy"].mean(),
#         result_df["Relevance"].mean(),
#         result_df["Hallucination"].mean(),
#         result_df["Completeness"].mean()
#     ]
#     agent_names = ["Accuracy", "Relevance", "Hallucination", "Completeness"]

#     plt.figure(figsize=(8, 4))
#     plt.bar(agent_names, average_scores)
#     plt.title("Average Agent Scores")
#     plt.xlabel("Agent")
#     plt.ylabel("Score")
#     plt.ylim(0, 100)
#     plt.tight_layout()
#     plt.savefig(os.path.join(BASE_DIR, "average_scores.png"), dpi=150)
#     plt.close()

#     # 3. Hallucination Frequency
#     plt.figure(figsize=(8, 4))
#     plt.bar(range(1, len(result_df) + 1), result_df["Hallucination"])
#     plt.title("Hallucination Scores")
#     plt.xlabel("Response")
#     plt.ylabel("Hallucination Score")
#     plt.ylim(0, 100)
#     plt.tight_layout()
#     plt.savefig(os.path.join(BASE_DIR, "hallucination.png"), dpi=150)
#     plt.close()

#     # 4. Quality Trend
#     plt.figure(figsize=(8, 4))
#     plt.plot(
#         range(1, len(result_df) + 1),
#         result_df["Overall Score"],
#         marker="o"
#     )
#     plt.title("Quality Trend")
#     plt.xlabel("Response")
#     plt.ylabel("Overall Score")
#     plt.ylim(0, 100)
#     plt.tight_layout()
#     plt.savefig(os.path.join(BASE_DIR, "quality_trend.png"), dpi=150)
#     plt.close()

#     # # =====================================================
#     # # DASHBOARD VISUALIZATIONS
#     # # =====================================================

#     # story.append(
#     #     Paragraph(
#     #         "Dashboard Visualizations",
#     #         heading_style
#     #     )
#     # )

#     # charts = [
#     #     (
#     #         "Verdict Distribution",
#     #         os.path.join(
#     #             BASE_DIR,
#     #             "verdict_distribution.png"
#     #         )
#     #     ),
#     #     (
#     #         "Average Agent Scores",
#     #         os.path.join(
#     #             BASE_DIR,
#     #             "average_scores.png"
#     #         )
#     #     ),
#     #     (
#     #         "Hallucination Frequency",
#     #         os.path.join(
#     #             BASE_DIR,
#     #             "hallucination.png"
#     #         )
#     #     ),
#     #     (
#     #         "Quality Trend",
#     #         os.path.join(
#     #             BASE_DIR,
#     #             "quality_trend.png"
#     #         )
#     #     ),
#     # ]

#     # # Put 2 charts on each page

#     # for i in range(0, len(charts), 2):

#     #     chart_rows = []

#     #     for title, chart_path in charts[i:i + 2]:

#     #         if os.path.exists(chart_path):

#     #             img = Image(chart_path)

#     #             img.drawWidth = 6.2 * inch
#     #             img.drawHeight = 3.1 * inch

#     #             chart_rows.append(
#     #                 KeepTogether([
#     #                     Paragraph(
#     #                         f"<b>{title}</b>",
#     #                         normal_style
#     #                     ),
#     #                     img,
#     #                     Spacer(1, 0.15 * inch)
#     #                 ])
#     #             )

#     #     for item in chart_rows:
#     #         story.append(item)

#     #     if i + 2 < len(charts):
#     #         story.append(PageBreak())

#     # story.append(PageBreak())
#     # =====================================================
# # DASHBOARD VISUALIZATIONS
# # =====================================================

#     story.append(
#     Paragraph(
#         "Dashboard Visualizations",
#         heading_style
#     )
# )

# # =====================================================
# # CREATE CURRENT CHART DATA FROM result_df
# # =====================================================

# # -------- 1. Verdict Distribution --------

#     verdict_order = [
#     "Pass",
#     "Needs Improvement",
#     "Fail"
# ]

#     verdict_counts = (
#     result_df["Verdict"]
#     .value_counts()
#     .reindex(verdict_order, fill_value=0)
# )
#     print("===== CHART DEBUG =====")
#     print(result_df[["Question", "Overall Score", "Verdict"]])
#     print("VERDICT COUNTS:")
#     print(verdict_counts)
#     print("=======================")

#     fig, ax = plt.subplots(figsize=(8, 4.5))

#     ax.bar(
#     verdict_counts.index,
#     verdict_counts.values
# )

#     ax.set_title("Verdict Distribution")
#     ax.set_xlabel("Verdict")
#     ax.set_ylabel("Count")

#     for i, value in enumerate(verdict_counts.values):
#         ax.text(
#         i,
#         value + 0.05,
#         str(value),
#         ha="center"
#     )

#     plt.tight_layout()

#     verdict_chart = os.path.join(
#     BASE_DIR,
#     "batch_verdict_distribution.png"
# )

#     fig.savefig(
#     verdict_chart,
#     dpi=150,
#     bbox_inches="tight"
# )

#     plt.close(fig)


# # =====================================================
# # 2. AVERAGE AGENT SCORES
# # =====================================================

#     average_scores = [
#     result_df["Accuracy"].mean(),
#     result_df["Relevance"].mean(),
#     result_df["Hallucination"].mean(),
#     result_df["Completeness"].mean()
# ]

#     agent_names = [
#     "Accuracy",
#     "Relevance",
#     "Hallucination",
#     "Completeness"
# ]

#     fig, ax = plt.subplots(figsize=(8, 4.5))

#     ax.bar(
#     agent_names,
#     average_scores
# )

#     ax.set_title("Average Agent Scores")
#     ax.set_xlabel("Agent")
#     ax.set_ylabel("Average Score")
#     ax.set_ylim(0, 100)

#     for i, value in enumerate(average_scores):
#         ax.text(
#         i,
#         value + 2,
#         f"{value:.2f}",
#         ha="center"
#     )

#     plt.tight_layout()

#     average_chart = os.path.join(
#     BASE_DIR,
#     "batch_average_scores.png"
# )

#     fig.savefig(
#     average_chart,
#     dpi=150,
#     bbox_inches="tight"
# )

#     plt.close(fig)


# # =====================================================
# # 3. HALLUCINATION FREQUENCY
# # =====================================================

#     no_hallucination = int(
#     (result_df["Hallucination"] == 100).sum()
# )

#     hallucination_found = (
#     len(result_df) - no_hallucination
# )

#     hallucination_values = [
#     no_hallucination,
#     hallucination_found
# ]

#     hallucination_labels = [
#     "No Hallucination",
#     "Hallucination Found"
# ]

#     fig, ax = plt.subplots(figsize=(7, 4.5))

#     ax.pie(
#     hallucination_values,
#     labels=hallucination_labels,
#     autopct="%1.0f%%",
#     startangle=90
# )

#     ax.set_title("Hallucination Frequency")

#     plt.tight_layout()

#     hallucination_chart = os.path.join(
#     BASE_DIR,
#     "batch_hallucination.png"
# )

#     fig.savefig(
#     hallucination_chart,
#     dpi=150,
#     bbox_inches="tight"
# )

#     plt.close(fig)


# # =====================================================
# # 4. QUALITY TREND
# # =====================================================

#     overall_scores = result_df["Overall Score"].tolist()

#     evaluations = list(
#     range(1, len(overall_scores) + 1)
# )

#     fig, ax = plt.subplots(figsize=(8, 4.5))

#     ax.plot(
#     evaluations,
#     overall_scores,
#     marker="o"
# )

#     ax.set_title("Quality Trend")
#     ax.set_xlabel("Evaluation")
#     ax.set_ylabel("Overall Score")
#     ax.set_ylim(0, 100)

#     plt.tight_layout()

#     quality_chart = os.path.join(
#     BASE_DIR,
#     "batch_quality_trend.png"
# )

#     fig.savefig(
#     quality_chart,
#     dpi=150,
#     bbox_inches="tight"
# )

#     plt.close(fig)


# # =====================================================
# # ADD CHARTS TO PDF
# # =====================================================

#     charts = [
#     (
#         "Verdict Distribution",
#         verdict_chart
#     ),
#     (
#         "Average Agent Scores",
#         average_chart
#     ),
#     (
#         "Hallucination Frequency",
#         hallucination_chart
#     ),
#     (
#         "Quality Trend",
#         quality_chart
#     )
# ]


# # Put 2 charts on each page

#     for i in range(0, len(charts), 2):

#         chart_rows = []

#         for title, chart_path in charts[i:i + 2]:

#             if os.path.exists(chart_path):

#                 img = Image(chart_path)

#                 img.drawWidth = 6.2 * inch
#                 img.drawHeight = 3.1 * inch

#                 chart_rows.append(
#                     KeepTogether([
#                     Paragraph(
#                         f"<b>{title}</b>",
#                         normal_style
#                     ),
#                     img,
#                     Spacer(
#                         1,
#                         0.15 * inch
#                     )
#                 ])
#             )

#     for item in chart_rows:
#         story.append(item)

#     if i + 2 < len(charts):
#         story.append(PageBreak())

#     story.append(PageBreak())

#     # =====================================================
#     # INDIVIDUAL EVALUATION RESULTS
#     # =====================================================

#     story.append(
#         Paragraph(
#             "Individual Evaluation Results",
#             heading_style
#         )
#     )

#     data = [
#         [
#             "Question",
#             "Acc",
#             "Rel",
#             "Hall",
#             "Comp",
#             "Overall",
#             "Verdict"
#         ]
#     ]

#     for _, row in result_df.iterrows():

#         question = str(row["Question"])

#         if len(question) > 42:
#             question = question[:42] + "..."

#         data.append([
#             Paragraph(question, small_style),
#             row["Accuracy"],
#             row["Relevance"],
#             row["Hallucination"],
#             row["Completeness"],
#             row["Overall Score"],
#             Paragraph(
#                 str(row["Verdict"]),
#                 small_style
#             )
#         ])

#     result_table = Table(
#         data,
#         colWidths=[
#             2.55 * inch,
#             0.48 * inch,
#             0.48 * inch,
#             0.48 * inch,
#             0.48 * inch,
#             0.62 * inch,
#             1.05 * inch
#         ],
#         repeatRows=1
#     )

#     result_table.setStyle(
#         TableStyle([
#             (
#                 "BACKGROUND",
#                 (0, 0),
#                 (-1, 0),
#                 colors.HexColor("#17365D")
#             ),
#             (
#                 "TEXTCOLOR",
#                 (0, 0),
#                 (-1, 0),
#                 colors.white
#             ),
#             (
#                 "FONTNAME",
#                 (0, 0),
#                 (-1, 0),
#                 "Helvetica-Bold"
#             ),
#             (
#                 "FONTSIZE",
#                 (0, 0),
#                 (-1, -1),
#                 7.5
#             ),
#             (
#                 "GRID",
#                 (0, 0),
#                 (-1, -1),
#                 0.5,
#                 colors.grey
#             ),
#             (
#                 "BACKGROUND",
#                 (0, 1),
#                 (-1, -1),
#                 colors.HexColor("#F8F9FA")
#             ),
#             (
#                 "ALIGN",
#                 (1, 0),
#                 (-1, -1),
#                 "CENTER"
#             ),
#             (
#                 "VALIGN",
#                 (0, 0),
#                 (-1, -1),
#                 "MIDDLE"
#             ),
#             (
#                 "TOPPADDING",
#                 (0, 0),
#                 (-1, -1),
#                 5
#             ),
#             (
#                 "BOTTOMPADDING",
#                 (0, 0),
#                 (-1, -1),
#                 5
#             ),
#         ])
#     )

#     story.append(result_table)

#     story.append(PageBreak())

#     # =====================================================
#     # FLAGGED RESPONSES
#     # =====================================================

#     story.append(
#         Paragraph(
#             "Flagged Responses",
#             heading_style
#         )
#     )

#     flagged = result_df[
#         result_df["Overall Score"] < 80
#     ]

#     if len(flagged) == 0:

#         story.append(
#             Paragraph(
#                 "No responses were flagged for improvement.",
#                 normal_style
#             )
#         )

#     else:

#         for _, row in flagged.iterrows():

#             question = str(row["Question"])

#             story.append(
#                 Paragraph(
#                     f"<b>Question:</b> {question}",
#                     normal_style
#                 )
#             )

#             story.append(
#                 Paragraph(
#                     f"<b>Overall Score:</b> "
#                     f"{row['Overall Score']}",
#                     normal_style
#                 )
#             )

#             story.append(
#                 Paragraph(
#                     f"<b>Verdict:</b> "
#                     f"{row['Verdict']}",
#                     normal_style
#                 )
#             )

#             story.append(
#                 Spacer(1, 0.15 * inch)
#             )

#     story.append(PageBreak())

#     # =====================================================
#     # IMPROVEMENT RECOMMENDATIONS
#     # =====================================================

#     story.append(
#         Paragraph(
#             "Improvement Recommendations",
#             heading_style
#         )
#     )

#     recommendations = [
#         "Improve factual correctness of AI responses.",
#         "Reduce hallucinated or unsupported statements.",
#         "Improve completeness of generated answers.",
#         "Validate responses using trusted reference information.",
#         "Improve response accuracy for low-scoring questions.",
#         "Continue monitoring evaluation consistency."
#     ]

#     for recommendation in recommendations:

#         story.append(
#             Paragraph(
#                 "• " + recommendation,
#                 normal_style
#             )
#         )

#     story.append(
#         Spacer(1, 0.3 * inch)
#     )

#     # =====================================================
#     # CONCLUSION
#     # =====================================================

#     story.append(
#         Paragraph(
#             "Conclusion",
#             heading_style
#         )
#     )

#     conclusion = f"""
#     The LLM Response Quality Evaluation System successfully
#     evaluated <b>{total}</b> AI-generated responses.

#     <br/><br/>

#     <b>Evaluation Summary</b>

#     <br/>
#     Passed: <b>{passed}</b>

#     <br/>
#     Needs Improvement: <b>{needs}</b>

#     <br/>
#     Failed: <b>{failed}</b>

#     <br/><br/>

#     Average Accuracy: <b>{avg_accuracy}</b>

#     <br/>
#     Average Relevance: <b>{avg_relevance}</b>

#     <br/>
#     Average Hallucination Score: <b>{avg_hallucination}</b>

#     <br/>
#     Average Completeness: <b>{avg_completeness}</b>

#     <br/>
#     Average Overall Score: <b>{avg_overall}</b>

#     <br/><br/>

#     The system provides a structured approach for evaluating
#     AI responses using multiple quality dimensions including
#     Accuracy, Relevance, Hallucination and Completeness.
#     """

#     story.append(
#         Paragraph(
#             conclusion,
#             normal_style
#         )
#     )

#     # =====================================================
#     # BUILD PDF
#     # =====================================================

#     doc.build(story)

#     return pdf_file

import os
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


# =========================================================
# GENERATE PDF
# =========================================================

def generate_pdf(result_df):

    # =====================================================
    # FILE LOCATION
    # =====================================================

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    pdf_file = os.path.join(
        BASE_DIR,
        "LLM_Evaluation_Report.pdf"
    )

    # =====================================================
    # CLEAN / COPY DATA
    # =====================================================

    df = result_df.copy()

    # Make sure verdict is always a clean string
    df["Verdict"] = (
        df["Verdict"]
        .astype(str)
        .str.strip()
    )

    # =====================================================
    # CALCULATE SUMMARY
    # =====================================================

    total = len(df)

    passed = int(
        (df["Verdict"] == "Pass").sum()
    )

    needs = int(
        (df["Verdict"] == "Needs Improvement").sum()
    )

    failed = int(
        (df["Verdict"] == "Fail").sum()
    )

    avg_accuracy = round(
        df["Accuracy"].mean(),
        2
    )

    avg_relevance = round(
        df["Relevance"].mean(),
        2
    )

    avg_hallucination = round(
        df["Hallucination"].mean(),
        2
    )

    avg_completeness = round(
        df["Completeness"].mean(),
        2
    )

    avg_overall = round(
        df["Overall Score"].mean(),
        2
    )

    # =====================================================
    # DEBUG
    # =====================================================

    print("\n========================================")
    print("PDF REPORT - CURRENT DATA")
    print("========================================")
    print(
        df[
            [
                "Question",
                "Accuracy",
                "Relevance",
                "Hallucination",
                "Completeness",
                "Overall Score",
                "Verdict",
            ]
        ].to_string(index=False)
    )
    print("----------------------------------------")
    print("Total:", total)
    print("Pass:", passed)
    print("Needs Improvement:", needs)
    print("Fail:", failed)
    print("Average Accuracy:", avg_accuracy)
    print("Average Relevance:", avg_relevance)
    print("Average Hallucination:", avg_hallucination)
    print("Average Completeness:", avg_completeness)
    print("Average Overall:", avg_overall)
    print("========================================\n")

    # =====================================================
    # PDF DOCUMENT
    # =====================================================

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35,
    )

    # =====================================================
    # STYLES
    # =====================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=8,
        spaceAfter=12,
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=8,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
    )

    story = []

    # =====================================================
    # COVER PAGE
    # =====================================================

    story.append(
        Spacer(
            1,
            0.7 * inch
        )
    )

    story.append(
        Paragraph(
            "LLM RESPONSE QUALITY<br/>"
            "EVALUATION REPORT",
            title_style,
        )
    )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )

    cover_data = [
        [
            "Project",
            "LLM Response Quality Evaluation System",
        ],
        [
            "Evaluation Mode",
            "Batch Evaluation",
        ],
        [
            "Total Responses",
            str(total),
        ],
        [
            "Generated On",
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
        ],
    ]

    cover_table = Table(
        cover_data,
        colWidths=[
            1.7 * inch,
            4.7 * inch,
        ],
    )

    cover_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#D9EAF7"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    story.append(cover_table)

    story.append(
        Spacer(
            1,
            0.6 * inch
        )
    )

    story.append(
        Paragraph(
            "This report presents the automated evaluation "
            "of AI-generated responses using Accuracy, "
            "Relevance, Hallucination and Completeness "
            "evaluation metrics.",
            normal_style,
        )
    )

    story.append(PageBreak())

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "Executive Summary",
            heading_style,
        )
    )

    summary_data = [
        ["Metric", "Value"],
        ["Total Evaluations", total],
        ["Passed", passed],
        ["Needs Improvement", needs],
        ["Failed", failed],
        ["Average Accuracy", avg_accuracy],
        ["Average Relevance", avg_relevance],
        [
            "Average Hallucination",
            avg_hallucination,
        ],
        [
            "Average Completeness",
            avg_completeness,
        ],
        [
            "Average Overall Score",
            avg_overall,
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            3.8 * inch,
            2.0 * inch,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#17365D"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#F4F7FA"),
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(summary_table)

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )

    story.append(
        Paragraph(
            f"""
            The system evaluated <b>{total}</b>
            AI-generated responses.

            A total of <b>{passed}</b> responses passed
            the evaluation, <b>{needs}</b> required
            improvement and <b>{failed}</b> failed.

            The average overall evaluation score was
            <b>{avg_overall}</b>.
            """,
            normal_style,
        )
    )

    story.append(PageBreak())

    # =====================================================
    # DASHBOARD VISUALIZATIONS
    # =====================================================

    story.append(
        Paragraph(
            "Dashboard Visualizations",
            heading_style,
        )
    )

    # =====================================================
    # 1. VERDICT DISTRIBUTION
    # =====================================================

    verdict_order = [
        "Pass",
        "Needs Improvement",
        "Fail",
    ]

    verdict_counts = (
        df["Verdict"]
        .value_counts()
        .reindex(
            verdict_order,
            fill_value=0,
        )
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        verdict_order,
        verdict_counts.values,
    )

    ax.set_title(
        "Verdict Distribution"
    )

    ax.set_xlabel(
        "Verdict"
    )

    ax.set_ylabel(
        "Number of Responses"
    )

    for i, value in enumerate(
        verdict_counts.values
    ):
        ax.text(
            i,
            float(value) + 0.05,
            str(int(value)),
            ha="center",
        )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    buffer.seek(0)

    story.append(
        Image(
            buffer,
            width=6.2 * inch,
            height=3.0 * inch,
        )
    )

    story.append(
        Spacer(
            1,
            0.2 * inch
        )
    )

    # =====================================================
    # 2. AVERAGE AGENT SCORES
    # =====================================================

    agent_names = [
        "Accuracy",
        "Relevance",
        "Hallucination",
        "Completeness",
    ]

    average_scores = [
        df["Accuracy"].mean(),
        df["Relevance"].mean(),
        df["Hallucination"].mean(),
        df["Completeness"].mean(),
    ]

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        agent_names,
        average_scores,
    )

    ax.set_title(
        "Average Agent Scores"
    )

    ax.set_xlabel(
        "Agent"
    )

    ax.set_ylabel(
        "Average Score"
    )

    ax.set_ylim(
        0,
        100
    )

    for i, value in enumerate(
        average_scores
    ):
        ax.text(
            i,
            float(value) + 2,
            f"{value:.2f}",
            ha="center",
        )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    buffer.seek(0)

    story.append(
        Image(
            buffer,
            width=6.2 * inch,
            height=3.0 * inch,
        )
    )

    story.append(PageBreak())

    # =====================================================
    # 3. HALLUCINATION SCORES
    # =====================================================

    story.append(
        Paragraph(
            "Hallucination Frequency",
            heading_style,
        )
    )

    evaluations = list(
        range(
            1,
            len(df) + 1,
        )
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.bar(
        evaluations,
        df["Hallucination"],
    )

    ax.set_title(
        "Hallucination Scores"
    )

    ax.set_xlabel(
        "Evaluation"
    )

    ax.set_ylabel(
        "Score"
    )

    ax.set_ylim(
        0,
        100,
    )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    buffer.seek(0)

    story.append(
        Image(
            buffer,
            width=6.2 * inch,
            height=3.0 * inch,
        )
    )

    story.append(
        Spacer(
            1,
            0.2 * inch
        )
    )

    # =====================================================
    # 4. QUALITY TREND
    # =====================================================

    story.append(
        Paragraph(
            "Quality Trend",
            heading_style,
        )
    )

    fig, ax = plt.subplots(
        figsize=(7, 4)
    )

    ax.plot(
        evaluations,
        df["Overall Score"],
        marker="o",
    )

    ax.set_title(
        "Quality Trend"
    )

    ax.set_xlabel(
        "Evaluation"
    )

    ax.set_ylabel(
        "Overall Score"
    )

    ax.set_ylim(
        0,
        100,
    )

    plt.tight_layout()

    buffer = BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    buffer.seek(0)

    story.append(
        Image(
            buffer,
            width=6.2 * inch,
            height=3.0 * inch,
        )
    )

    story.append(PageBreak())

    # =====================================================
    # INDIVIDUAL EVALUATION RESULTS
    # =====================================================

    story.append(
        Paragraph(
            "Individual Evaluation Results",
            heading_style,
        )
    )

    data = [
        [
            "Question",
            "Acc",
            "Rel",
            "Hall",
            "Comp",
            "Overall",
            "Verdict",
        ]
    ]

    for _, row in df.iterrows():

        question = str(
            row["Question"]
        )

        if len(question) > 42:
            question = (
                question[:42]
                + "..."
            )

        data.append(
            [
                Paragraph(
                    question,
                    small_style,
                ),
                row["Accuracy"],
                row["Relevance"],
                row["Hallucination"],
                row["Completeness"],
                row["Overall Score"],
                Paragraph(
                    str(row["Verdict"]),
                    small_style,
                ),
            ]
        )

    result_table = Table(
        data,
        colWidths=[
            2.55 * inch,
            0.48 * inch,
            0.48 * inch,
            0.48 * inch,
            0.48 * inch,
            0.62 * inch,
            1.05 * inch,
        ],
        repeatRows=1,
    )

    result_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#17365D"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7.5,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#F8F9FA"),
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(
        result_table
    )

    story.append(PageBreak())

    # =====================================================
    # FLAGGED RESPONSES
    # =====================================================

    story.append(
        Paragraph(
            "Flagged Responses",
            heading_style,
        )
    )

    flagged = df[
        df["Overall Score"] < 80
    ]

    if len(flagged) == 0:

        story.append(
            Paragraph(
                "No responses were flagged "
                "for improvement.",
                normal_style,
            )
        )

    else:

        for _, row in flagged.iterrows():

            question = str(
                row["Question"]
            )

            story.append(
                Paragraph(
                    f"<b>Question:</b> "
                    f"{question}",
                    normal_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Overall Score:</b> "
                    f"{row['Overall Score']}",
                    normal_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Verdict:</b> "
                    f"{row['Verdict']}",
                    normal_style,
                )
            )

            story.append(
                Spacer(
                    1,
                    0.15 * inch
                )
            )

    story.append(PageBreak())

    # =====================================================
    # IMPROVEMENT RECOMMENDATIONS
    # =====================================================

    story.append(
        Paragraph(
            "Improvement Recommendations",
            heading_style,
        )
    )

    recommendations = [
        "Improve factual correctness of AI responses.",
        "Reduce hallucinated or unsupported statements.",
        "Improve completeness of generated answers.",
        "Validate responses using trusted reference information.",
        "Improve response accuracy for low-scoring questions.",
        "Continue monitoring evaluation consistency.",
    ]

    for recommendation in recommendations:

        story.append(
            Paragraph(
                "• " + recommendation,
                normal_style,
            )
        )

    story.append(
        Spacer(
            1,
            0.3 * inch
        )
    )

    # =====================================================
    # CONCLUSION
    # =====================================================

    story.append(
        Paragraph(
            "Conclusion",
            heading_style,
        )
    )

    conclusion = f"""
    The LLM Response Quality Evaluation System
    successfully evaluated <b>{total}</b>
    AI-generated responses.

    <br/><br/>

    <b>Evaluation Summary</b>

    <br/>
    Passed: <b>{passed}</b>

    <br/>
    Needs Improvement: <b>{needs}</b>

    <br/>
    Failed: <b>{failed}</b>

    <br/><br/>

    Average Accuracy: <b>{avg_accuracy}</b>

    <br/>
    Average Relevance: <b>{avg_relevance}</b>

    <br/>
    Average Hallucination Score:
    <b>{avg_hallucination}</b>

    <br/>
    Average Completeness:
    <b>{avg_completeness}</b>

    <br/>
    Average Overall Score:
    <b>{avg_overall}</b>

    <br/><br/>

    The system provides a structured approach
    for evaluating AI responses using multiple
    quality dimensions including Accuracy,
    Relevance, Hallucination and Completeness.
    """

    story.append(
        Paragraph(
            conclusion,
            normal_style,
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)

    return pdf_file
