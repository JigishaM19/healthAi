import os
import shutil
import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from models import MedicalDocument, Medication, HealthProfile
from services.ocr_service import extract_text_from_file
from services.document_classifier import classify_document
from services.document_parser import extract_structured_data
from services.report_analyzer import analyze_medical_document
from services.timeline_service import create_event
from services.trend_analysis_service import ingest_lab_measurements
from services.health_memory_service import create_memory_entry

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024 # 20 MB

async def process_document_upload(file: UploadFile, user_id: int, db: Session) -> MedicalDocument:
    # 1. Validate File Size & Extension
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 20 MB."
        )

    ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
    allowed_exts = ['pdf', 'doc', 'docx', 'rtf', 'txt', 'csv', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'webp', 'tif', 'tiff', 'bmp', 'heic', 'heif']
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '.{ext}'. Supported formats: {', '.join(allowed_exts)}"
        )

    # 2. Save file securely to backend/uploads/
    unique_name = f"doc_{user_id}_{int(datetime.datetime.utcnow().timestamp())}.{ext}"
    saved_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Create initial document record
    doc_record = MedicalDocument(
        user_id=user_id,
        file_name=file.filename,
        file_type=ext,
        file_path=saved_path,
        document_type="general_medical"
    )
    db.add(doc_record)
    db.commit()
    db.refresh(doc_record)

    # 4. Extract Text (OCR / Document Parser)
    extracted_text = extract_text_from_file(saved_path, ext)
    doc_record.extracted_text = extracted_text

    # 5. Classify Document Type
    classification = classify_document(extracted_text, file.filename)
    doc_record.document_type = classification["document_type"]

    # 6. Parse Structured Data
    structured_data = await extract_structured_data(extracted_text, classification["document_type"])
    doc_record.structured_data = structured_data

    # 7. Fetch User Health Profile for Context & Conflict Check
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    profile_dict = {}
    if profile:
        profile_dict = {
            "conditions": profile.conditions or [],
            "allergies": profile.allergies or [],
            "medications": profile.medications or []
        }

    # 8. AI Medical Analysis
    ai_analysis = await analyze_medical_document(
        extracted_text=extracted_text,
        document_type=classification["document_type"],
        structured_data=structured_data,
        user_profile=profile_dict
    )
    
    doc_record.ai_summary = ai_analysis["summary"]
    doc_record.abnormal_values = ai_analysis.get("abnormal_values", [])
    doc_record.analyzed_at = datetime.datetime.utcnow()

    # Dispatch notification for document upload & analysis complete
    try:
        from services.notification_service import dispatch_notification
        await dispatch_notification(db, user_id, "document_uploaded", {"file_name": file.filename})
        await dispatch_notification(db, user_id, "report_analyzed", {
            "file_name": file.filename,
            "summary": ai_analysis["summary"]
        })
    except Exception as ne:
        print("[ReportService] Notification dispatch error:", ne)

    # 8.5 Generate PDF Medical Report automatically
    try:
        from services.pdf_generator import generate_pdf_report
        await generate_pdf_report(db, doc_record.id)
    except Exception as pdfe:
        print(f"[ReportService] PDF Generation error for document {doc_record.id}:", pdfe)

    # 9. Update User Medication List & Medications Table if medicines detected
    extracted_meds = structured_data.get("medicines", [])
    if extracted_meds:
        for med in extracted_meds:
            med_name = med.get("name")
            if med_name:
                # Add to medications table
                existing_med = db.query(Medication).filter(
                    Medication.user_id == user_id,
                    Medication.medicine_name == med_name
                ).first()
                if not existing_med:
                    new_med = Medication(
                        user_id=user_id,
                        medicine_name=med_name,
                        dosage=med.get("dosage", "5mg"),
                        frequency=med.get("frequency", "Once daily"),
                        duration=med.get("duration", "30 days"),
                        prescribing_doctor=structured_data.get("doctor_info", {}).get("name", "Prescribing Doctor")
                    )
                    db.add(new_med)

                # Append to HealthProfile medications list if not present
                if profile:
                    current_meds = list(profile.medications or [])
                    if med_name not in current_meds:
                        current_meds.append(med_name)
                        profile.medications = current_meds

    # 10. Automatically Create Health Timeline Event with specialized details
    try:
        doc_type = classification['document_type']
        abnormal_count = len(ai_analysis.get("abnormal_values", []))
        med_names = [m.get("name") for m in extracted_meds if m.get("name")]

        # Determine document-specific title and summary
        if doc_type == "lab_report":
            title_text = f"Lab Report Uploaded: {file.filename}"
            summary_text = f"{ai_analysis['summary']} ({abnormal_count} abnormal lab values detected)."
        elif doc_type == "prescription":
            title_text = f"Prescription Imported: {file.filename}"
            first_med = med_names[0] if med_names else "Prescription medicines"
            summary_text = f"{first_med} & medication schedule processed and active."
        elif doc_type == "medicine_photo":
            title_text = f"Medicine Identified: {file.filename}"
            summary_text = f"{', '.join(med_names) if med_names else 'Medication'} recognized from uploaded photo."
        elif doc_type == "discharge_summary":
            title_text = f"Hospital Discharge Summary Added: {file.filename}"
            hosp = structured_data.get("doctor_info", {}).get("hospital", "Hospital")
            summary_text = f"{hosp} discharge report analyzed and added to medical history."
        elif doc_type == "imaging_report":
            title_text = f"MRI / X-ray Report Reviewed: {file.filename}"
            summary_text = f"Imaging report analyzed by HealthAI. Summary: {ai_analysis['summary']}"
        elif doc_type == "vaccination_record":
            title_text = f"Vaccination Record Imported: {file.filename}"
            summary_text = f"Immunization records updated."
        elif doc_type == "insurance_document":
            title_text = f"Insurance Document Processed: {file.filename}"
            summary_text = f"Insurance & claim document filed."
        else:
            title_text = f"Medical Document Processed: {file.filename}"
            summary_text = ai_analysis['summary']

        if ai_analysis.get("warnings"):
            summary_text += " " + " ".join(ai_analysis["warnings"])

        create_event(
            db=db,
            user_id=user_id,
            event_type="report",
            title=title_text,
            summary=summary_text,
            details={
                "document_id": doc_record.id,
                "file_name": file.filename,
                "file_type": ext,
                "document_type": doc_type,
                "abnormal_values": ai_analysis.get("abnormal_values", []),
                "extracted_medicines": med_names,
                "extracted_text_preview": extracted_text[:300] if extracted_text else "",
                "doctor_info": structured_data.get("doctor_info", {}),
                "ai_summary": ai_analysis.get("summary", ""),
                "warnings": ai_analysis.get("warnings", [])
            }
        )
    except Exception as te:
        print(f"[ReportService] Timeline event creation error: {te}")

    # 11. Ingest Lab Measurements & Record Health Memory Entry
    try:
        ingest_lab_measurements(
            db=db,
            user_id=user_id,
            document_id=doc_record.id,
            abnormal_values=doc_record.abnormal_values or [],
            structured_data=structured_data
        )

        create_memory_entry(
            db=db,
            user_id=user_id,
            memory_type=doc_type,
            title=title_text,
            summary=ai_analysis['summary'],
            source_type="medical_document",
            source_id=doc_record.id,
            metadata_json={
                "file_name": file.filename,
                "document_type": doc_type,
                "abnormal_count": abnormal_count
            }
        )
    except Exception as me:
        print(f"[ReportService] Memory/Trend ingestion error: {me}")

    db.commit()
    db.refresh(doc_record)
    return doc_record
