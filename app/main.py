from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil
import os

from app.ai_engine import build_vector_store, answer_question
from app.parser import parse_questionnaire
from app.exporter import export_answers

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Store generated answers
stored_results = []


# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


# Upload questionnaire
@app.post("/upload_questionnaire")
async def upload_questionnaire(file: UploadFile = File(...)):

    os.makedirs("uploads", exist_ok=True)

    path = "uploads/questionnaire.csv"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Questionnaire uploaded"}


# Upload reference documents
@app.post("/upload_reference")
async def upload_reference(file: UploadFile = File(...)):

    os.makedirs("references", exist_ok=True)

    path = f"references/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Reference uploaded"}


# Generate answers
@app.post("/generate")
def generate_answers(request: Request):

    global stored_results

    questionnaire_path = "uploads/questionnaire.csv"

    questions = parse_questionnaire(questionnaire_path)

    index, chunks, sources = build_vector_store()

    results = []

    for q in questions:

        answer, citation, evidence = answer_question(q, index, chunks, sources)

        evidence_text = evidence[0][0][:250]

        results.append({
            "question": q,
            "answer": answer,
            "citation": citation,
            "confidence": "High",
            "evidence": evidence_text
        })

    stored_results = results

    answered = 0
    not_found = 0

    for r in results:
        if r["answer"] == "Not found in references.":
            not_found += 1
        else:
            answered += 1

    summary = {
        "total": len(results),
        "answered": answered,
        "not_found": not_found
    }

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "results": results,
            "summary": summary
        }
    )


# Export answers
@app.get("/export")
def export():

    export_answers(stored_results)

    return FileResponse(
        "answers.docx",
        filename="questionnaire_answers.docx"
    )