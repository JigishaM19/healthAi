import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database import get_db
from models import User, MedicalDocument, Medication
from auth import get_current_user
from services.report_service import process_document_upload
from services.document_classifier import classify_document
from services.ocr_service import extract_text_from_file
from services.report_analyzer import analyze_medical_document

router = APIRouter(tags=["Universal Medical Document Intelligence"])

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload any medical document format (PDF, DOCX, CSV, XLSX, JPG, PNG, WEBP, etc.).
    Runs full OCR text extraction, classification, structured entity parsing, AI analysis & allergy conflict check.
    """
    doc_record = await process_document_upload(file, current_user.id, db)
    return {
        "document_id": doc_record.id,
        "file_name": doc_record.file_name,
        "file_type": doc_record.file_type,
        "document_type": doc_record.document_type,
        "summary": doc_record.ai_summary,
        "status": "processed"
    }

@router.post("/documents/{id}/extract")
def extract_document(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not doc.extracted_text and os.path.exists(doc.file_path):
        doc.extracted_text = extract_text_from_file(doc.file_path, doc.file_type)
        classification = classify_document(doc.extracted_text, doc.file_name)
        doc.document_type = classification["document_type"]
        db.commit()

    return {
        "document_id": doc.id,
        "file_name": doc.file_name,
        "document_type": doc.document_type,
        "extracted_text": doc.extracted_text,
        "structured_data": doc.structured_data
    }

@router.post("/documents/{id}/analyze")
async def analyze_document(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    profile = current_user.health_profile
    profile_dict = {
        "conditions": profile.conditions or [] if profile else [],
        "allergies": profile.allergies or [] if profile else [],
        "medications": profile.medications or [] if profile else []
    }

    ai_res = await analyze_medical_document(
        extracted_text=doc.extracted_text or doc.file_name,
        document_type=doc.document_type,
        structured_data=doc.structured_data or {},
        user_profile=profile_dict
    )

    doc.ai_summary = ai_res["summary"]
    doc.abnormal_values = ai_res.get("abnormal_values", [])
    db.commit()

    return {
        "document_id": doc.id,
        "summary": ai_res["summary"],
        "document_type": doc.document_type,
        "abnormal_values": ai_res.get("abnormal_values", []),
        "medications": doc.structured_data.get("medicines", []),
        "recommendations": ai_res.get("recommendations", []),
        "red_flags": ai_res.get("red_flags", []),
        "warnings": ai_res.get("warnings", [])
    }

@router.get("/documents")
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    docs = db.query(MedicalDocument).filter(
        MedicalDocument.user_id == current_user.id
    ).order_by(MedicalDocument.created_at.desc()).all()
    return docs

@router.get("/documents/{id}")
def get_document(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/documents/{id}/download")
def download_document(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()
    if not doc or not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(doc.file_path, filename=doc.file_name)

@router.delete("/documents/{id}")
def delete_document(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    db.delete(doc)
    db.commit()
    return {"message": "Medical document deleted successfully"}

@router.get("/medications")
def list_medications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    meds = db.query(Medication).filter(
        Medication.user_id == current_user.id
    ).order_by(Medication.created_at.desc()).all()

    # Fallback to health profile medications list if table is empty
    if not meds and current_user.health_profile and current_user.health_profile.medications:
        meds = []
        for m in current_user.health_profile.medications:
            meds.append({
                "id": len(meds) + 1,
                "user_id": current_user.id,
                "medicine_name": m,
                "dosage": "As prescribed",
                "frequency": "Daily",
                "duration": "Ongoing",
                "active": "active",
                "created_at": datetime.datetime.utcnow().isoformat()
            })
    return meds


@router.get("/documents/{id}/pdf")
async def get_document_pdf(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if not doc.pdf_generated or not doc.pdf_report_path or not os.path.exists(doc.pdf_report_path):
        from services.pdf_generator import generate_pdf_report
        await generate_pdf_report(db, doc.id)
        db.refresh(doc)

    if not os.path.exists(doc.pdf_report_path):
        raise HTTPException(status_code=404, detail="PDF report file could not be rendered")

    media_type = "application/pdf"
    if doc.pdf_report_path.endswith(".html"):
        media_type = "text/html"

    return FileResponse(
        path=doc.pdf_report_path,
        media_type=media_type,
        filename=f"HealthAI_Report_{doc.id}.pdf"
    )


@router.post("/documents/{id}/generate-pdf")
async def force_generate_pdf(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(MedicalDocument).filter(
        MedicalDocument.id == id,
        MedicalDocument.user_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    from services.pdf_generator import generate_pdf_report
    pdf_path = await generate_pdf_report(db, doc.id)

    return {
        "message": "PDF report regenerated successfully",
        "document_id": doc.id,
        "pdf_path": pdf_path,
        "generated_at": doc.pdf_generated_at.isoformat() if doc.pdf_generated_at else None
    }

