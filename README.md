# LLM Response Quality Evaluator

## Project Overview

The LLM Response Quality Evaluator evaluates AI-generated responses using a Retrieval-Augmented Generation (RAG) pipeline and multiple LLM Judge Agents. The system retrieves a trusted reference answer from a knowledge base and evaluates the AI response based on Accuracy, Relevance, and Hallucination.

---

## Features

- Evaluation Input Module
- Streamlit Frontend
- FastAPI Backend
- RAG Knowledge Base
- ChromaDB Vector Database
- Semantic Retrieval
- Multi-Agent Response Evaluation
- Validation Framework
- CSV Report Generation

---

## Judge Agents

### Accuracy Judge Agent
- Evaluates factual correctness.
- Compares AI response with the retrieved reference answer.
- Returns:
  - Accuracy Score
  - Reason

### Relevance Judge Agent
- Checks whether the AI response answers the user's question.
- Returns:
  - Relevance Score
  - Reason

### Hallucination Detection Agent
- Detects unsupported or fabricated information.
- Identifies hallucinated statements.
- Returns:
  - Hallucination Score
  - Reason
  - Hallucinated Statement

---

## RAG Pipeline

1. Load TruthfulQA Dataset
2. Chunk Documents
3. Generate Embeddings
4. Store Embeddings in ChromaDB
5. Retrieve Relevant Reference Answer
6. Send Reference Answer to Judge Agents

---

## Tech Stack

- Python
- Streamlit
- FastAPI
- Ollama (Llama 3)
- ChromaDB
- Sentence Transformers
- LangChain
- Pandas

---

## Validation

Validation performed on multiple benchmark-style question-answer pairs.

Validation includes:

- Correct Answers
- Incorrect Answers
- Hallucinated Answers
- Unrelated Answers
- Paraphrased Answers

Validation results are automatically saved to:

validation_results.csv

---

## Current Progress

### Milestone 1

- ✅ Dataset Loader
- ✅ Document Chunking
- ✅ Embedding Generation
- ✅ ChromaDB Integration
- ✅ Semantic Retrieval (RAG)

### Milestone 2

- ✅ Accuracy Judge Agent
- ✅ Relevance Judge Agent
- ✅ Hallucination Detection Agent
- ✅ Hallucinated Statement Detection
- ✅ Validation Script
- ✅ Validation Results (CSV)
- ✅ FastAPI Integration
- ✅ Streamlit Integration

---

## Project Structure

```
LLM-Evaluation-system/

├── agents/
├── backend/
├── frontend/
├── rag/
├── datasets/
├── database/
├── tests/
├── validation_results.csv
└── README.md
```

---

## Future Enhancements

- Overall Score Agent
- Report Generation Agent
- Support for additional benchmark datasets
- Enhanced analytics dashboard