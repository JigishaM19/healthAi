from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from database import get_db
from models import User
from auth import get_current_user
from services.medication_safety_service import run_medication_safety_audit
from services.interaction_checker import check_drug_drug_interactions
from services.food_interaction_engine import check_food_medication_interactions
from services.medication_scheduler import generate_medication_schedule
from services.pdf_generator import generate_pdf_from_html

router = APIRouter(tags=["Medication Safety Intelligence Engine"])

class CheckInteractionsInput(BaseModel):
    medications: List[str]

class AnalyzePrescriptionInput(BaseModel):
    extracted_medications: List[str]
    document_id: Optional[int] = None

@router.post("/medications/check-interactions")
def check_interactions_endpoint(
    input_data: CheckInteractionsInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyzes input medication list for drug-drug, food-drug, condition, and lab interactions.
    """
    return run_medication_safety_audit(db, current_user.id, custom_medications=input_data.medications)

@router.get("/medications/safety-report")
def get_safety_report_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates personalized Medication Safety Intelligence report incorporating profile, prescriptions, labs, and conditions.
    """
    return run_medication_safety_audit(db, current_user.id)

@router.get("/medications/schedule")
def get_medication_schedule_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns daily medication timing schedule with meal relations and spacing rules.
    """
    report = run_medication_safety_audit(db, current_user.id)
    return {
        "schedule": report.get("medication_schedule", []),
        "disclaimer": report.get("safety_disclaimer")
    }

@router.post("/medications/analyze-prescription")
def analyze_prescription_endpoint(
    input_data: AnalyzePrescriptionInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Immediately analyzes extracted prescription medications against existing profile medications and lab values.
    """
    return run_medication_safety_audit(db, current_user.id, custom_medications=input_data.extracted_medications)

@router.get("/medications/safety-report/pdf")
def download_safety_report_pdf(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates and downloads a printable Medication Safety Report PDF.
    """
    report = run_medication_safety_audit(db, current_user.id)

    meds_str = ", ".join(report.get("medications_analyzed", []))
    dd_items = "".join([f"<li><strong>{i['severity']} Severity</strong>: {', '.join(i['medications'])} — {i['description']}</li>" for i in report.get("drug_drug_interactions", [])])
    fd_items = "".join([f"<li><strong>{i['severity']} Severity</strong>: {i['medication']} + {i['conflicting_food']} — {i['description']}</li>" for i in report.get("food_interactions", [])])
    sched_items = "".join([f"<li><strong>{s['time']}</strong>: {s['medication']} ({s['meal_relation']}) — <em>{s['spacing_rule']}</em></li>" for s in report.get("medication_schedule", [])])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Medication Safety Intelligence Report</title>
        <style>
            body {{ font-family: Helvetica, Arial, sans-serif; margin: 30px; color: #1e293b; }}
            h1 {{ color: #0284c7; border-bottom: 2px solid #0284c7; padding-bottom: 8px; }}
            h2 {{ color: #0f172a; margin-top: 20px; border-bottom: 1px solid #cbd5e1; }}
            .badge {{ display: inline-block; padding: 4px 12px; font-weight: bold; border-radius: 4px; background: #fee2e2; color: #991b1b; }}
            .disclaimer {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; margin-top: 30px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>HealthAI Medication Safety Intelligence Report</h1>
        <p><strong>Patient Name:</strong> {report.get('user_name')}</p>
        <p><strong>Generated At:</strong> {report.get('generated_at')}</p>
        <p><strong>Overall Risk Severity:</strong> <span class="badge">{report.get('overall_severity')}</span></p>

        <h2>Analyzed Medications</h2>
        <p>{meds_str}</p>

        <h2>Drug-Drug Interactions</h2>
        <ul>{dd_items if dd_items else "<li>No significant drug-drug interactions detected.</li>"}</ul>

        <h2>Food & Dietary Interactions</h2>
        <ul>{fd_items if fd_items else "<li>No active food-medication conflicts detected.</li>"}</ul>

        <h2>Daily Medication Schedule</h2>
        <ul>{sched_items if sched_items else "<li>Schedule clear.</li>"}</ul>

        <div class="disclaimer">
            <strong>Medical Safety Disclaimer:</strong> {report.get('safety_disclaimer')}
        </div>
    </body>
    </html>
    """

    pdf_bytes = generate_pdf_from_html(html_content)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=Medication_Safety_Report_User_{current_user.id}.pdf"
    })
