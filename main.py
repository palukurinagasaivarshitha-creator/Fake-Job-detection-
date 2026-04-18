from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Fake Job Detection API Running 🚀"}


# 🔍 Detect company name
def detect_company(text):
    match = re.search(r'company[:\-]\s*([A-Za-z][A-Za-z0-9 &.]+)', text, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r'at\s+([A-Za-z][A-Za-z &.]+)', text)
    if match:
        return match.group(1)

    return "Not Mentioned"


# 🔗 Generate verification links
def get_links(company):
    q = company.replace(" ", "+")
    return {
        "google": f"https://www.google.com/search?q={q}+careers",
        "linkedin": f"https://www.linkedin.com/jobs/search/?keywords={q}"
    }


# 🚀 Main prediction API
@app.post("/predict")
def predict(job: JobInput):

    text = job.text.lower()
    score = 0
    reasons = []

    if "whatsapp" in text:
        score += 3
        reasons.append("Uses WhatsApp communication")

    if "earn" in text and "per day" in text:
        score += 3
        reasons.append("Unrealistic salary")

    if "urgent" in text:
        score += 1
        reasons.append("Urgency pressure")

    if "no experience" in text:
        score += 1
        reasons.append("No experience required")

    company = detect_company(job.text)

    if score >= 4:
        result = "FAKE JOB ❌"
        risk = "HIGH RISK"
    elif score >= 2:
        result = "SUSPICIOUS ⚠️"
        risk = "MEDIUM RISK"
    else:
        result = "REAL JOB ✅"
        risk = "LOW RISK"

    return {
        "prediction": result,
        "risk": risk,
        "company": company,
        "reasons": reasons,
        "links": get_links(company)
    }
