from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    KeepTogether
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

import os
from datetime import datetime


# =========================================================
# GENERATE PDF
# =========================================================

def generate_pdf(result_df):

    # -----------------------------------------------------
    # File locations
    # -----------------------------------------------------

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    pdf_file = os.path.join(
        BASE_DIR,
        "LLM_Evaluation_Report.pdf"
    )

    # -----------------------------------------------------
    # PDF document
    # -----------------------------------------------------

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    # -----------------------------------------------------
    # Styles
    # -----------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=8,
        spaceAfter=12
    )

    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        spaceAfter=8
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )

    story = []

    # =====================================================
    # CALCULATE SUMMARY
    # =====================================================

    total = len(result_df)

    passed = len(
        result_df[result_df["Verdict"] == "Pass"]
    )

    needs = len(
        result_df[
            result_df["Verdict"] == "Needs Improvement"
        ]
    )

    failed = len(
        result_df[result_df["Verdict"] == "Fail"]
    )

    avg_accuracy = round(
        result_df["Accuracy"].mean(), 2
    )

    avg_relevance = round(
        result_df["Relevance"].mean(), 2
    )

    avg_hallucination = round(
        result_df["Hallucination"].mean(), 2
    )

    avg_completeness = round(
        result_df["Completeness"].mean(), 2
    )

    avg_overall = round(
        result_df["Overall Score"].mean(), 2
    )

    # =====================================================
    # COVER PAGE
    # =====================================================

    story.append(Spacer(1, 0.7 * inch))

    story.append(
        Paragraph(
            "LLM RESPONSE QUALITY<br/>"
            "EVALUATION REPORT",
            title_style
        )
    )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    cover_data = [
        ["Project", "LLM Response Quality Evaluation System"],
        ["Evaluation Mode", "Batch Evaluation"],
        ["Total Responses", str(total)],
        [
            "Generated On",
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        ],
    ]

    cover_table = Table(
        cover_data,
        colWidths=[1.7 * inch, 4.7 * inch]
    )

    cover_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#D9EAF7")
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
        ])
    )

    story.append(cover_table)

    story.append(
        Spacer(1, 0.6 * inch)
    )

    story.append(
        Paragraph(
            "This report presents the automated evaluation "
            "of AI-generated responses using Accuracy, "
            "Relevance, Hallucination and Completeness "
            "evaluation metrics.",
            normal_style
        )
    )

    story.append(PageBreak())

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "Executive Summary",
            heading_style
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
        ["Average Hallucination", avg_hallucination],
        ["Average Completeness", avg_completeness],
        ["Average Overall Score", avg_overall],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[3.8 * inch, 2.0 * inch]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#17365D")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#F4F7FA")
            ),
            (
                "ALIGN",
                (1, 1),
                (1, -1),
                "CENTER"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(summary_table)

    story.append(
        Spacer(1, 0.3 * inch)
    )

    # Short summary paragraph

    story.append(
        Paragraph(
            f"""
            The system evaluated <b>{total}</b> AI-generated
            responses. A total of <b>{passed}</b> responses
            passed the evaluation, <b>{needs}</b> required
            improvement and <b>{failed}</b> failed.
            The average overall evaluation score was
            <b>{avg_overall}</b>.
            """,
            normal_style
        )
    )

    story.append(PageBreak())

    # =====================================================
    # DASHBOARD VISUALIZATIONS
    # =====================================================

    story.append(
        Paragraph(
            "Dashboard Visualizations",
            heading_style
        )
    )

    charts = [
        (
            "Verdict Distribution",
            os.path.join(
                BASE_DIR,
                "verdict_distribution.png"
            )
        ),
        (
            "Average Agent Scores",
            os.path.join(
                BASE_DIR,
                "average_scores.png"
            )
        ),
        (
            "Hallucination Frequency",
            os.path.join(
                BASE_DIR,
                "hallucination.png"
            )
        ),
        (
            "Quality Trend",
            os.path.join(
                BASE_DIR,
                "quality_trend.png"
            )
        ),
    ]

    # Put 2 charts on each page

    for i in range(0, len(charts), 2):

        chart_rows = []

        for title, chart_path in charts[i:i + 2]:

            if os.path.exists(chart_path):

                img = Image(chart_path)

                img.drawWidth = 6.2 * inch
                img.drawHeight = 3.1 * inch

                chart_rows.append(
                    KeepTogether([
                        Paragraph(
                            f"<b>{title}</b>",
                            normal_style
                        ),
                        img,
                        Spacer(1, 0.15 * inch)
                    ])
                )

        for item in chart_rows:
            story.append(item)

        if i + 2 < len(charts):
            story.append(PageBreak())

    story.append(PageBreak())

    # =====================================================
    # INDIVIDUAL EVALUATION RESULTS
    # =====================================================

    story.append(
        Paragraph(
            "Individual Evaluation Results",
            heading_style
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
            "Verdict"
        ]
    ]

    for _, row in result_df.iterrows():

        question = str(row["Question"])

        if len(question) > 42:
            question = question[:42] + "..."

        data.append([
            Paragraph(question, small_style),
            row["Accuracy"],
            row["Relevance"],
            row["Hallucination"],
            row["Completeness"],
            row["Overall Score"],
            Paragraph(
                str(row["Verdict"]),
                small_style
            )
        ])

    result_table = Table(
        data,
        colWidths=[
            2.55 * inch,
            0.48 * inch,
            0.48 * inch,
            0.48 * inch,
            0.48 * inch,
            0.62 * inch,
            1.05 * inch
        ],
        repeatRows=1
    )

    result_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#17365D")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7.5
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#F8F9FA")
            ),
            (
                "ALIGN",
                (1, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
        ])
    )

    story.append(result_table)

    story.append(PageBreak())

    # =====================================================
    # FLAGGED RESPONSES
    # =====================================================

    story.append(
        Paragraph(
            "Flagged Responses",
            heading_style
        )
    )

    flagged = result_df[
        result_df["Overall Score"] < 80
    ]

    if len(flagged) == 0:

        story.append(
            Paragraph(
                "No responses were flagged for improvement.",
                normal_style
            )
        )

    else:

        for _, row in flagged.iterrows():

            question = str(row["Question"])

            story.append(
                Paragraph(
                    f"<b>Question:</b> {question}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Overall Score:</b> "
                    f"{row['Overall Score']}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Verdict:</b> "
                    f"{row['Verdict']}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 0.15 * inch)
            )

    story.append(PageBreak())

    # =====================================================
    # IMPROVEMENT RECOMMENDATIONS
    # =====================================================

    story.append(
        Paragraph(
            "Improvement Recommendations",
            heading_style
        )
    )

    recommendations = [
        "Improve factual correctness of AI responses.",
        "Reduce hallucinated or unsupported statements.",
        "Improve completeness of generated answers.",
        "Validate responses using trusted reference information.",
        "Improve response accuracy for low-scoring questions.",
        "Continue monitoring evaluation consistency."
    ]

    for recommendation in recommendations:

        story.append(
            Paragraph(
                "• " + recommendation,
                normal_style
            )
        )

    story.append(
        Spacer(1, 0.3 * inch)
    )

    # =====================================================
    # CONCLUSION
    # =====================================================

    story.append(
        Paragraph(
            "Conclusion",
            heading_style
        )
    )

    conclusion = f"""
    The LLM Response Quality Evaluation System successfully
    evaluated <b>{total}</b> AI-generated responses.

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
    Average Hallucination Score: <b>{avg_hallucination}</b>

    <br/>
    Average Completeness: <b>{avg_completeness}</b>

    <br/>
    Average Overall Score: <b>{avg_overall}</b>

    <br/><br/>

    The system provides a structured approach for evaluating
    AI responses using multiple quality dimensions including
    Accuracy, Relevance, Hallucination and Completeness.
    """

    story.append(
        Paragraph(
            conclusion,
            normal_style
        )
    )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(story)

    return pdf_file
