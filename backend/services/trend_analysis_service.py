import datetime
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from models import LabMeasurement, TimelineEvent
from services.health_memory_service import create_memory_entry
from services.timeline_service import create_event

def ingest_lab_measurements(
    db: Session,
    user_id: int,
    document_id: Optional[int],
    abnormal_values: List[Dict[str, Any]],
    structured_data: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Stores extracted lab values into lab_measurements table, performs comparative trend analysis
    against previous measurements, and creates Timeline Insight Events & Health Memory entries.
    """
    trend_results = []
    
    # Gather lab items from abnormal_values list & structured_data
    items_to_process = list(abnormal_values or [])
    
    # Parse items from structured_data if available
    if structured_data and isinstance(structured_data, dict):
        if "lab_results" in structured_data and isinstance(structured_data["lab_results"], list):
            for lr in structured_data["lab_results"]:
                if isinstance(lr, dict) and lr.get("name"):
                    items_to_process.append(lr)

    seen_names = set()
    for item in items_to_process:
        test_name = item.get("name") or item.get("test_name")
        if not test_name or test_name in seen_names:
            continue
        seen_names.add(test_name)

        # Parse numerical value
        raw_val = item.get("value")
        val_float = None
        if isinstance(raw_val, (int, float)):
            val_float = float(raw_val)
        elif isinstance(raw_val, str):
            # Extract digits and decimal point
            cleaned = "".join([c for c in raw_val if c.isdigit() or c == '.'])
            try:
                val_float = float(cleaned) if cleaned else None
            except ValueError:
                val_float = None

        if val_float is None:
            continue

        unit = item.get("unit", "")
        ref_range = item.get("reference") or item.get("reference_range", "")
        status = item.get("status", "Normal")

        # 1. Look up previous measurement for comparative trend analysis
        prev_measurement = db.query(LabMeasurement).filter(
            LabMeasurement.user_id == user_id,
            LabMeasurement.test_name == test_name
        ).order_by(LabMeasurement.test_date.desc()).first()

        # 2. Insert new measurement record
        new_measurement = LabMeasurement(
            user_id=user_id,
            document_id=document_id,
            test_name=test_name,
            value=val_float,
            unit=unit,
            reference_range=ref_range,
            status=status,
            test_date=datetime.datetime.utcnow()
        )
        db.add(new_measurement)
        db.commit()
        db.refresh(new_measurement)

        # 3. Compute comparative trend if previous record exists
        if prev_measurement:
            prev_val = prev_measurement.value
            diff = round(val_float - prev_val, 2)
            pct_change = round((diff / prev_val) * 100, 1) if prev_val != 0 else 0.0

            # Determine direction & clinical category
            # Tests where a decrease is positive (Cholesterol, Glucose, CRP, Triglycerides, LDL)
            lower_is_better_tests = ["cholesterol", "ldl", "glucose", "hba1c", "triglycerides", "crp", "sgpt", "sgot", "creatinine", "urea"]
            test_lower = test_name.lower()

            if any(k in test_lower for k in lower_is_better_tests):
                trend_dir = "Improving" if diff < 0 else ("Worsening" if diff > 0 else "Stable")
            else: # Tests where an increase is positive (Hemoglobin, Vitamin D, Vitamin B12, RBC, Platelets)
                trend_dir = "Improving" if diff > 0 else ("Worsening" if diff < 0 else "Stable")

            if abs(pct_change) < 3.0:
                trend_dir = "Stable"

            trend_info = {
                "test": test_name,
                "latest": val_float,
                "previous": prev_val,
                "change": diff,
                "percent_change": pct_change,
                "trend": trend_dir,
                "unit": unit
            }
            trend_results.append(trend_info)

            # 4. Generate Automatic Timeline Insight Event & Health Memory for significant changes
            if trend_dir in ["Improving", "Worsening"]:
                title_text = f"{test_name} {trend_dir}: {val_float} {unit}"
                verb = "decreased" if diff < 0 else "increased"
                summary_text = f"{test_name} {verb} by {abs(diff)} {unit} ({abs(pct_change)}% change) compared to previous report."

                # Create Timeline Insight Event
                create_event(
                    db=db,
                    user_id=user_id,
                    event_type="report",
                    title=title_text,
                    summary=summary_text,
                    details=trend_info
                )

                # Create Health Memory Record
                create_memory_entry(
                    db=db,
                    user_id=user_id,
                    memory_type="lab_trend",
                    title=title_text,
                    summary=summary_text,
                    source_type="lab_measurement",
                    source_id=new_measurement.id,
                    metadata_json=trend_info
                )

    return trend_results


def get_tracked_trends(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Computes trend metrics for all lab tests belonging to the user.
    """
    measurements = db.query(LabMeasurement).filter(
        LabMeasurement.user_id == user_id
    ).order_by(LabMeasurement.test_date.asc()).all()

    grouped: Dict[str, List[LabMeasurement]] = {}
    for m in measurements:
        if m.test_name not in grouped:
            grouped[m.test_name] = []
        grouped[m.test_name].append(m)

    trends_summary = {}
    for name, list_m in grouped.items():
        if len(list_m) >= 2:
            prev = list_m[-2]
            latest = list_m[-1]
            diff = round(latest.value - prev.value, 2)
            pct = round((diff / prev.value) * 100, 1) if prev.value != 0 else 0.0

            lower_is_better = ["cholesterol", "ldl", "glucose", "hba1c", "triglycerides", "crp", "sgpt", "sgot", "creatinine"]
            test_lower = name.lower()
            if any(k in test_lower for k in lower_is_better):
                direction = "Improving" if diff < 0 else ("Worsening" if diff > 0 else "Stable")
            else:
                direction = "Improving" if diff > 0 else ("Worsening" if diff < 0 else "Stable")

            if abs(pct) < 3.0:
                direction = "Stable"

            trends_summary[name] = {
                "latest": latest.value,
                "previous": prev.value,
                "change": diff,
                "percent_change": pct,
                "trend": direction,
                "unit": latest.unit or ""
            }
        elif len(list_m) == 1:
            m = list_m[0]
            trends_summary[name] = {
                "latest": m.value,
                "previous": None,
                "change": 0,
                "percent_change": 0,
                "trend": "Baseline Recorded",
                "unit": m.unit or ""
            }

    return trends_summary


def get_test_history(db: Session, user_id: int, test_name: str) -> Dict[str, Any]:
    """
    Returns full chronological history of a specific lab parameter.
    """
    records = db.query(LabMeasurement).filter(
        LabMeasurement.user_id == user_id,
        LabMeasurement.test_name.ilike(f"%{test_name}%")
    ).order_by(LabMeasurement.test_date.asc()).all()

    history = []
    for r in records:
        history.append({
            "id": r.id,
            "date": r.test_date.strftime("%Y-%m-%d") if r.test_date else None,
            "value": r.value,
            "unit": r.unit,
            "status": r.status,
            "reference_range": r.reference_range
        })

    return {
        "test": test_name,
        "history": history
    }
