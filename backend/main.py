# # from fastapi import FastAPI
# from fastapi import FastAPI, Form, UploadFile, File
# from pydantic import BaseModel
# from concurrent.futures import ThreadPoolExecutor
# from rag.retrieval import retrieve

# from agents.accuracy_agent import evaluate_accuracy
# from agents.relevance_agent import evaluate_relevance
# from agents.hallucination_agent import evaluate_hallucination
# from agents.completeness_agent import evaluate_completeness
# from agents.verdict_agent import evaluate_verdict
# import os
# from rag.pdf_reference import create_pdf_reference, retrieve_from_pdf
# app = FastAPI(title="LLM Evaluation System")


# class EvaluationRequest(BaseModel):
#     question: str
#     ai_response: str
# class BatchEvaluationRequest(BaseModel):
#     evaluations: list[EvaluationRequest]


# @app.get("/")
# def home():
#     return {
#         "message": "LLM Evaluation Backend Running"
#     }


# # @app.post("/evaluate")
# # def evaluate(data: EvaluationRequest):

# #     # Retrieve reference information
# #     retrieved = retrieve(data.question)

# #     reference_answer = retrieved["reference_answer"]
# #     retrieved_question = retrieved["question"]
# #     category = retrieved["category"]

# #     # Run Accuracy Agent
# #     accuracy = evaluate_accuracy(
# #         retrieved_question,
# #         reference_answer,
# #         data.ai_response
# #     )

# #     # Run Relevance Agent
# #     relevance = evaluate_relevance(
# #         retrieved_question,
# #         reference_answer,
# #         data.ai_response
# #     )

# #     # Run Hallucination Agent
# #     hallucination = evaluate_hallucination(
# #         retrieved_question,
# #         reference_answer,
# #         data.ai_response
# #     )

# #     completeness = evaluate_completeness(
# #         data.question,
# #         data.ai_response,
# #         reference_answer
# #     )

# #     verdict = evaluate_verdict(
# #     accuracy,
# #     relevance,
# #     hallucination,
# #     completeness
# # )
# #     print("Question:", data.question)
# #     print("Reference:", reference_answer)
# #     print("AI Response:", data.ai_response)
# #     print("-" * 60)

# #     return {
# #         "status": "success",

# #         "question": data.question,

# #         "ai_response": data.ai_response,

# #         "reference_answer": reference_answer,

# #         "category": category,

# #         "accuracy": accuracy,

# #         "relevance": relevance,

# #         "hallucination": hallucination,

# #         "completeness": completeness,

# #         "verdict": verdict
# #     }
# @app.post("/evaluate")
# async def evaluate(
#     question: str = Form(...),
#     ai_response: str = Form(...),
#     reference_pdf: UploadFile = File(None)
# ):

#     # ============================================
#     # GET REFERENCE
#     # ============================================

#     if reference_pdf is not None:

#         # ----------------------------------------
#         # Save uploaded PDF temporarily
#         # ----------------------------------------

#         pdf_path = os.path.join(
#             "database",
#             reference_pdf.filename
#         )

#         os.makedirs(
#             "database",
#             exist_ok=True
#         )

#         contents = await reference_pdf.read()

#         with open(pdf_path, "wb") as f:
#             f.write(contents)

#         # ----------------------------------------
#         # Create PDF embeddings
#         # ----------------------------------------

#         create_pdf_reference(pdf_path)

#         # ----------------------------------------
#         # Retrieve from uploaded PDF
#         # ----------------------------------------

#         reference_answer = retrieve_from_pdf(
#             question
#         )

#         retrieved_question = question

#         category = "Uploaded PDF"

#     else:

#         # ----------------------------------------
#         # EXISTING RAG DATASET
#         # ----------------------------------------

#         retrieved = retrieve(question)

#         reference_answer = retrieved[
#             "reference_answer"
#         ]

#         retrieved_question = retrieved[
#             "question"
#         ]

#         category = retrieved[
#             "category"
#         ]

#     # ============================================
#     # ACCURACY
#     # ============================================

#     accuracy = evaluate_accuracy(
#         retrieved_question,
#         reference_answer,
#         ai_response
#     )

#     # ============================================
#     # RELEVANCE
#     # ============================================

#     relevance = evaluate_relevance(
#         retrieved_question,
#         reference_answer,
#         ai_response
#     )

#     # ============================================
#     # HALLUCINATION
#     # ============================================

#     hallucination = evaluate_hallucination(
#         retrieved_question,
#         reference_answer,
#         ai_response
#     )

#     # ============================================
#     # COMPLETENESS
#     # ============================================

#     completeness = evaluate_completeness(
#         question,
#         ai_response,
#         reference_answer
#     )

#     # ============================================
#     # VERDICT
#     # ============================================

#     verdict = evaluate_verdict(
#         accuracy,
#         relevance,
#         hallucination,
#         completeness
#     )

#     # ============================================
#     # RETURN
#     # ============================================

#     return {

#         "status": "success",

#         "question": question,

#         "ai_response": ai_response,

#         "reference_answer": reference_answer,

#         "category": category,

#         "accuracy": accuracy,

#         "relevance": relevance,

#         "hallucination": hallucination,

#         "completeness": completeness,

#         "verdict": verdict
#     }
# @app.post("/batch_evaluate")
# def batch_evaluate(data: BatchEvaluationRequest):

#     # ============================================
#     # FUNCTION TO EVALUATE ONE RESPONSE
#     # ============================================

#     def evaluate_one(item):

#         # --------------------------------------------
#         # Retrieve reference information
#         # --------------------------------------------

#         retrieved = retrieve(item.question)

#         reference_answer = retrieved["reference_answer"]
#         retrieved_question = retrieved["question"]
#         category = retrieved["category"]

#         # --------------------------------------------
#         # Accuracy Agent
#         # --------------------------------------------

#         accuracy = evaluate_accuracy(
#             retrieved_question,
#             reference_answer,
#             item.ai_response
#         )

#         # --------------------------------------------
#         # Relevance Agent
#         # --------------------------------------------

#         relevance = evaluate_relevance(
#             retrieved_question,
#             reference_answer,
#             item.ai_response
#         )

#         # --------------------------------------------
#         # Hallucination Agent
#         # --------------------------------------------

#         hallucination = evaluate_hallucination(
#             retrieved_question,
#             reference_answer,
#             item.ai_response
#         )

#         # --------------------------------------------
#         # Completeness Agent
#         # --------------------------------------------

#         completeness = evaluate_completeness(
#             item.question,
#             item.ai_response,
#             reference_answer
#         )

#         # --------------------------------------------
#         # Verdict Agent
#         # --------------------------------------------

#         verdict = evaluate_verdict(
#             accuracy,
#             relevance,
#             hallucination,
#             completeness
#         )

#         # --------------------------------------------
#         # Return result
#         # --------------------------------------------

#         return {
#             "question": item.question,
#             "ai_response": item.ai_response,
#             "reference_answer": reference_answer,
#             "category": category,
#             "accuracy": accuracy,
#             "relevance": relevance,
#             "hallucination": hallucination,
#             "completeness": completeness,
#             "verdict": verdict
#         }


#     # ============================================
#     # PARALLEL BATCH PROCESSING
#     # ============================================

#     results = []

#     # Maximum 4 responses evaluated simultaneously
#     with ThreadPoolExecutor(max_workers=4) as executor:

#         results = list(
#             executor.map(
#                 evaluate_one,
#                 data.evaluations
#             )
#         )


#     # ============================================
#     # RETURN RESPONSE
#     # ============================================

#     return {
#         "status": "success",
#         "total_records": len(results),
#         "results": results
#     }
# # @app.post("/batch_evaluate")
# # def batch_evaluate(data: BatchEvaluationRequest):

# #     results = []

# #     for item in data.evaluations:

# #         # Retrieve reference information
# #         retrieved = retrieve(item.question)

# #         reference_answer = retrieved["reference_answer"]
# #         retrieved_question = retrieved["question"]
# #         category = retrieved["category"]

# #         # Run Accuracy Agent
# #         accuracy = evaluate_accuracy(
# #             retrieved_question,
# #             reference_answer,
# #             item.ai_response
# #         )

# #         # Run Relevance Agent
# #         relevance = evaluate_relevance(
# #             retrieved_question,
# #             reference_answer,
# #             item.ai_response
# #         )

# #         # Run Hallucination Agent
# #         hallucination = evaluate_hallucination(
# #             retrieved_question,
# #             reference_answer,
# #             item.ai_response
# #         )

# #         # Run Completeness Agent
# #         completeness = evaluate_completeness(
# #             item.question,
# #             item.ai_response,
# #             reference_answer
# #         )

# #         # Run Verdict Agent
# #         verdict = evaluate_verdict(
# #             accuracy,
# #             relevance,
# #             hallucination,
# #             completeness
# #         )

# #         # Store result
# #         results.append({
# #             "question": item.question,
# #             "ai_response": item.ai_response,
# #             "reference_answer": reference_answer,
# #             "category": category,
# #             "accuracy": accuracy,
# #             "relevance": relevance,
# #             "hallucination": hallucination,
# #             "completeness": completeness,
# #             "verdict": verdict
# #         })

# #     return {
# #         "status": "success",
# #         "total_records": len(results),
# #         "results": results
# #     }

from fastapi import FastAPI, UploadFile, File, Form
from jsonschema.exceptions import relevance
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from rag.retrieval import retrieve

from agents.accuracy_agent import evaluate_accuracy
from agents.relevance_agent import evaluate_relevance
from agents.hallucination_agent import evaluate_hallucination
from agents.completeness_agent import evaluate_completeness
from agents.verdict_agent import evaluate_verdict

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np


app = FastAPI(title="LLM Evaluation System")


# ============================================================
# LOAD EMBEDDING MODEL FOR PDF RETRIEVAL
# ============================================================

print("Loading embedding model...")

pdf_embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)

print("Embedding model loaded!")


# ============================================================
# NORMAL EVALUATION MODEL
# ============================================================

class EvaluationRequest(BaseModel):
    question: str
    ai_response: str


class BatchEvaluationRequest(BaseModel):
    evaluations: list[EvaluationRequest]


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# CHUNK PDF TEXT
# ============================================================

def chunk_text(text, chunk_size=500, overlap=100):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ============================================================
# RETRIEVE REFERENCE FROM PDF
# ============================================================

def retrieve_from_pdf(question, pdf_file):

    print("\nProcessing uploaded PDF...")

    # Extract PDF text
    text = extract_pdf_text(pdf_file)
    import re
    text = re.sub(r'\s+', ' ', text).strip()
    if not text.strip():
        raise ValueError(
            "The uploaded PDF does not contain readable text."
        )

    print("PDF text extracted.")

    # Create chunks
    chunks = chunk_text(text)

    print("Total PDF chunks:", len(chunks))

    if not chunks:
        raise ValueError(
            "No readable content was found in the PDF."
        )

    # Generate embeddings
    chunk_embeddings = pdf_embedding_model.encode(
        chunks,
        normalize_embeddings=True
    )

    # Question embedding
    question_embedding = pdf_embedding_model.encode(
        question,
        normalize_embeddings=True
    )

    # Cosine similarity
    similarities = np.dot(
        chunk_embeddings,
        question_embedding
    )

    # Best matching chunk
    best_index = int(np.argmax(similarities))

    best_chunk = chunks[best_index]

    best_score = float(similarities[best_index])

    print("\n========== PDF RETRIEVAL ==========")

    print("Question:", question)

    print("Similarity:", best_score)

    print("Reference:", best_chunk)

    print("-" * 60)

    return {
        "reference_answer": best_chunk,
        "question": question,
        "category": "Uploaded PDF"
    }


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "LLM Evaluation Backend Running"
    }


# ============================================================
# SINGLE EVALUATION
# ============================================================

@app.post("/evaluate")
async def evaluate(
    question: str = Form(...),
    ai_response: str = Form(...),
    reference_pdf: UploadFile | None = File(None)
):

    try:

        # ====================================================
        # IF PDF IS UPLOADED
        # ====================================================

        if reference_pdf is not None:

            print("\n📄 Uploaded PDF:", reference_pdf.filename)

            retrieved = retrieve_from_pdf(
                question,
                reference_pdf.file
            )

        # ====================================================
        # IF NO PDF IS UPLOADED
        # ====================================================

        else:

            print("\n📚 Using TruthfulQA RAG...")

            retrieved = retrieve(question)


        # ====================================================
        # REFERENCE INFORMATION
        # ====================================================

        reference_answer = retrieved["reference_answer"]

        retrieved_question = retrieved["question"]

        category = retrieved["category"]


        # ====================================================
        # ACCURACY AGENT
        # ====================================================

        accuracy = evaluate_accuracy(
            retrieved_question,
            reference_answer,
            ai_response
        )


        # ====================================================
        # RELEVANCE AGENT
        # ====================================================

        relevance = evaluate_relevance(
            retrieved_question,
            reference_answer,
            ai_response
        )


        # ====================================================
        # HALLUCINATION AGENT
        # ====================================================

        hallucination = evaluate_hallucination(
            retrieved_question,
            reference_answer,
            ai_response
        )


        # ====================================================
        # COMPLETENESS AGENT
        # ====================================================

        completeness = evaluate_completeness(
            question,
            ai_response,
            reference_answer
        )

        # ====================================================
        # VERDICT AGENT
        # ====================================================

        verdict = evaluate_verdict(
            accuracy,
            relevance,
            hallucination,
            completeness
        )


        print("\nQuestion:", question)

        print("Reference:", reference_answer)

        print("AI Response:", ai_response)

        print("-" * 60)


        # ====================================================
        # RETURN RESULT
        # ====================================================

        return {

            "status": "success",

            "question": question,

            "ai_response": ai_response,

            "reference_answer": reference_answer,

            "category": category,

            "accuracy": accuracy,

            "relevance": relevance,

            "hallucination": hallucination,

            "completeness": completeness,

            "verdict": verdict
        }


    except Exception as e:

        print("ERROR:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# BATCH EVALUATION
# ============================================================

@app.post("/batch_evaluate")
def batch_evaluate(data: BatchEvaluationRequest):


    # ========================================================
    # FUNCTION TO EVALUATE ONE RESPONSE
    # ========================================================

    def evaluate_one(item):

        retrieved = retrieve(item.question)

        reference_answer = retrieved["reference_answer"]

        retrieved_question = retrieved["question"]

        category = retrieved["category"]


        accuracy = evaluate_accuracy(
            retrieved_question,
            reference_answer,
            item.ai_response
        )


        relevance = evaluate_relevance(
            retrieved_question,
            reference_answer,
            item.ai_response
        )


        hallucination = evaluate_hallucination(
            retrieved_question,
            reference_answer,
            item.ai_response
        )


        completeness = evaluate_completeness(
            item.question,
            item.ai_response,
            reference_answer
        )


        verdict = evaluate_verdict(
            accuracy,
            relevance,
            hallucination,
            completeness
        )


        return {

            "question": item.question,

            "ai_response": item.ai_response,

            "reference_answer": reference_answer,

            "category": category,

            "accuracy": accuracy,

            "relevance": relevance,

            "hallucination": hallucination,

            "completeness": completeness,

            "verdict": verdict
        }


    # ========================================================
    # PARALLEL PROCESSING
    # ========================================================

    with ThreadPoolExecutor(max_workers=4) as executor:

        results = list(
            executor.map(
                evaluate_one,
                data.evaluations
            )
        )


    return {

        "status": "success",

        "total_records": len(results),

        "results": results
    }