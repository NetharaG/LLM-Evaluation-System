import time
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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




app = FastAPI(title="LLM Evaluation System")


# ============================================================
# LOAD EMBEDDING MODEL FOR PDF RETRIEVAL
# ============================================================

# print("Loading embedding model...")

# pdf_embedding_model = SentenceTransformer(
#     "all-MiniLM-L6-v2",
#     local_files_only=True
# )

# print("Embedding model loaded!")


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

    # --------------------------------------------------------
    # Extract PDF text
    # --------------------------------------------------------

    text = extract_pdf_text(pdf_file)

    import re

    text = re.sub(r'\s+', ' ', text).strip()

    if not text:
        raise ValueError(
            "The uploaded PDF does not contain readable text."
        )

    print("PDF text extracted.")

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    chunks = chunk_text(text)

    print("Total PDF chunks:", len(chunks))

    if not chunks:
        raise ValueError(
            "No readable content was found in the PDF."
        )

    # --------------------------------------------------------
    # TF-IDF retrieval
    # --------------------------------------------------------

    documents = chunks + [question]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(documents)

    chunk_vectors = vectors[:-1]
    question_vector = vectors[-1]

    similarities = cosine_similarity(
        question_vector,
        chunk_vectors
    )[0]

    # --------------------------------------------------------
    # Best matching chunk
    # --------------------------------------------------------

    best_index = int(similarities.argmax())

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
# ============================================================
# BATCH EVALUATION
# ============================================================

def call_with_retry(function, *args, max_retries=3):

    for attempt in range(max_retries):

        try:
            result = function(*args)

            # Small delay between Groq requests
            time.sleep(2)

            return result

        except Exception as e:

            error_message = str(e)

            # Handle Groq rate limit
            if "429" in error_message or "RateLimitError" in error_message:

                wait_time = 5 * (attempt + 1)

                print(
                    f"Groq rate limit reached. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

    raise Exception(
        "Groq rate limit exceeded after multiple retries."
    )


@app.post("/batch_evaluate")
def batch_evaluate(data: BatchEvaluationRequest):

    results = []

    # ========================================================
    # SEQUENTIAL BATCH PROCESSING
    # ========================================================
    #
    # IMPORTANT:
    # Do NOT use ThreadPoolExecutor here.
    #
    # Each CSV row uses 5 judge agents.
    # Processing sequentially prevents too many
    # Groq requests from being sent simultaneously.
    # ========================================================

    for index, item in enumerate(data.evaluations):

        print(
            f"===== Evaluating row {index + 1} "
            f"of {len(data.evaluations)} ====="
        )

        try:

            # ------------------------------------------------
            # RETRIEVAL
            # ------------------------------------------------

            retrieved = retrieve(item.question)

            reference_answer = retrieved["reference_answer"]

            retrieved_question = retrieved["question"]

            category = retrieved["category"]


            # ------------------------------------------------
            # ACCURACY
            # ------------------------------------------------

            accuracy = call_with_retry(
                evaluate_accuracy,
                retrieved_question,
                reference_answer,
                item.ai_response
            )


            # ------------------------------------------------
            # RELEVANCE
            # ------------------------------------------------

            relevance = call_with_retry(
                evaluate_relevance,
                retrieved_question,
                reference_answer,
                item.ai_response
            )


            # ------------------------------------------------
            # HALLUCINATION
            # ------------------------------------------------

            hallucination = call_with_retry(
                evaluate_hallucination,
                retrieved_question,
                reference_answer,
                item.ai_response
            )


            # ------------------------------------------------
            # COMPLETENESS
            # ------------------------------------------------

            completeness = call_with_retry(
                evaluate_completeness,
                item.question,
                item.ai_response,
                reference_answer
            )


            # ------------------------------------------------
            # VERDICT
            # ------------------------------------------------

            verdict = call_with_retry(
                evaluate_verdict,
                accuracy,
                relevance,
                hallucination,
                completeness
            )


            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            results.append({

                "question": item.question,

                "ai_response": item.ai_response,

                "reference_answer": reference_answer,

                "category": category,

                "accuracy": accuracy,

                "relevance": relevance,

                "hallucination": hallucination,

                "completeness": completeness,

                "verdict": verdict
            })


            print(
                f"===== Row {index + 1} completed successfully ====="
            )


        except Exception as e:

            print(
                f"===== Row {index + 1} FAILED ====="
            )

            print(str(e))

            # Keep the batch going instead of failing
            # the entire CSV.

            results.append({

                "question": item.question,

                "ai_response": item.ai_response,

                "reference_answer": "",

                "category": "",

                "accuracy": {
                    "agent": "Accuracy",
                    "score": 0,
                    "reason": "Evaluation failed."
                },

                "relevance": {
                    "agent": "Relevance",
                    "score": 0,
                    "reason": "Evaluation failed."
                },

                "hallucination": {
                    "agent": "Hallucination",
                    "score": 0,
                    "reason": "Evaluation failed."
                },

                "completeness": {
                    "agent": "Completeness",
                    "score": 0,
                    "reason": "Evaluation failed."
                },

                "verdict": {
                    "overall_score": 0,
                    "verdict": "Error",
                    "summary": str(e)
                }
            })


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "status": "success",

        "total_records": len(results),

        "results": results
    }
# @app.post("/batch_evaluate")
# def batch_evaluate(data: BatchEvaluationRequest):


#     # ========================================================
#     # FUNCTION TO EVALUATE ONE RESPONSE
#     # ========================================================

#     def evaluate_one(item):

#         retrieved = retrieve(item.question)

#         reference_answer = retrieved["reference_answer"]

#         retrieved_question = retrieved["question"]

#         category = retrieved["category"]


#         accuracy = evaluate_accuracy(
#             retrieved_question,
#             reference_answer,
#             item.ai_response
#         )


#         relevance = evaluate_relevance(
#             retrieved_question,
#             reference_answer,
#             item.ai_response
#         )


#         hallucination = evaluate_hallucination(
#             retrieved_question,
#             reference_answer,
#             item.ai_response
#         )


#         completeness = evaluate_completeness(
#             item.question,
#             item.ai_response,
#             reference_answer
#         )


#         verdict = evaluate_verdict(
#             accuracy,
#             relevance,
#             hallucination,
#             completeness
#         )


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


#     # ========================================================
#     # PARALLEL PROCESSING
#     # ========================================================

#     with ThreadPoolExecutor(max_workers=4) as executor:

#         results = list(
#             executor.map(
#                 evaluate_one,
#                 data.evaluations
#             )
#         )


#     return {

#         "status": "success",

#         "total_records": len(results),

#         "results": results
#     }