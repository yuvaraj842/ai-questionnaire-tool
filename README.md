# AI Questionnaire Answering Tool

## Overview

This project is a web application that automates answering structured questionnaires (security reviews, compliance forms, vendor assessments) using internal reference documents.

The system uses a **Retrieval-Augmented Generation (RAG)** approach: questions are parsed, relevant content is retrieved from reference documents using vector search, and answers are generated with citations and evidence.


## Industry Context

**Industry:** SaaS Security & Compliance

**Fictional Company:** SecureCloud AI
SecureCloud AI provides cloud security monitoring and compliance automation tools for enterprise infrastructure.

## Features

* User authentication
* Upload questionnaire (CSV)
* Upload reference documents
* Question parsing
* Semantic retrieval using embeddings
* AI-generated answers with citations
* Evidence snippets
* Confidence score
* Coverage summary
* Export completed questionnaire (.docx)


## Architecture

Upload Questionnaire
        ↓
Parse Questions
        ↓
Embed Reference Documents
        ↓
FAISS Vector Search
        ↓
Retrieve Relevant Context
        ↓
Generate Answers
        ↓
Add Citation + Evidence
        ↓
Display Results
        ↓
Export Document

## Tech Stack

Backend:

* Python
* FastAPI

AI & Retrieval:

* Sentence Transformers
* FAISS

Data Processing:

* Pandas

Authentication:

* Passlib
* JWT

Frontend:

* HTML
* Jinja2

Export:

* python-docx

Deployment:

* Render

## Project Structure

app/
  main.py
  ai_engine.py
  parser.py
  exporter.py
  auth.py
  database.py

templates/
  login.html
  dashboard.html
  results.html

references/
uploads/

requirements.txt
README.md

## Run Locally

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000


## Deployment

The application can be deployed on Render.

Start command:


uvicorn app.main:app --host 0.0.0.0 --port 10000


## Author

Yuvaraj SJ
