import os
import datetime
from sqlalchemy.orm import Session
from models import MedicalDocument
from services.pdf_template_service import build_pdf_context
from services.timeline_service import create_event

GENERATED_REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_reports")
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

if not os.path.exists(GENERATED_REPORTS_DIR):
    os.makedirs(GENERATED_REPORTS_DIR, exist_ok=True)

def render_html_report(context: dict) -> str:
    template_path = os.path.join(TEMPLATES_DIR, "report_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template_str = f.read()
    
    try:
        from jinja2 import Template
        template = Template(template_str)
        return template.render(**context)
    except ImportError:
        # Pure Python fallback renderer if Jinja2 package is not installed
        res = template_str
        res = res.replace("{{ document_id }}", str(context.get("document_id", "")))
        res = res.replace("{{ generated_date }}", str(context.get("generated_date", "")))
        res = res.replace("{{ user_name }}", str(context.get("user_name", "")))
        res = res.replace("{{ age }}", str(context.get("age", "")))
        res = res.replace("{{ gender }}", str(context.get("gender", "")))
        res = res.replace("{{ conditions_str }}", str(context.get("conditions_str", "")))
        res = res.replace("{{ allergies_str }}", str(context.get("allergies_str", "")))
        res = res.replace("{{ file_name }}", str(context.get("file_name", "")))
        res = res.replace("{{ document_type }}", str(context.get("document_type", "")))
        res = res.replace("{{ upload_date }}", str(context.get("upload_date", "")))
        res = res.replace("{{ ai_summary }}", str(context.get("ai_summary", "")))

        # Render lab results table
        lab_rows = ""
        for lab in context.get("lab_results", []):
            st_cls = "status-normal"
            if lab.get("status") == "High":
                st_cls = "status-high"
            elif lab.get("status") == "Low":
                st_cls = "status-low"
            lab_rows += f"""<tr>
              <td><strong>{lab.get('name')}</strong></td>
              <td>{lab.get('value')}</td>
              <td>{lab.get('unit')}</td>
              <td>{lab.get('reference')}</td>
              <td><span class="{st_cls}">{lab.get('status', 'NORMAL').upper()}</span></td>
            </tr>"""
        
        # Simple string replacement for Jinja loops
        if "{% if lab_results %}" in res and "{% endif %}" in res:
            part1 = res.split("{% if lab_results %}")[0]
            part2 = res.split("{% endif %}")[1]
            if lab_rows:
                table_html = f"""<div class="section-title">Extracted Laboratory Results</div>
                <table class="med-table">
                  <thead><tr><th>Marker / Test Name</th><th>Measured Value</th><th>Unit</th><th>Reference Range</th><th>Clinical Status</th></tr></thead>
                  <tbody>{lab_rows}</tbody>
                </table>"""
                res = part1 + table_html + part2
            else:
                res = part1 + part2

        # Render medicines table
        med_rows = ""
        for med in context.get("medicines", []):
            med_rows += f"""<tr>
              <td><strong>{med.get('name')}</strong></td>
              <td>{med.get('dosage')}</td>
              <td>{med.get('frequency')}</td>
              <td>{med.get('duration')}</td>
              <td>{med.get('instructions')}</td>
            </tr>"""

        if "{% if medicines %}" in res and "{% endif %}" in res:
            parts = res.split("{% if medicines %}")
            part1 = parts[0]
            part2 = res.split("{% endif %}")[2] if len(res.split("{% endif %}")) > 2 else res.split("{% endif %}")[-1]
            if med_rows:
                table_html = f"""<div class="section-title">Extracted Prescription Schedule</div>
                <table class="med-table">
                  <thead><tr><th>Medicine Name</th><th>Dosage</th><th>Frequency</th><th>Duration</th><th>Instructions</th></tr></thead>
                  <tbody>{med_rows}</tbody>
                </table>"""
                res = part1 + table_html + part2

        # Render warnings box
        warn_li = "".join([f"<li>{w}</li>" for w in context.get("warnings", [])])
        if "{% if warnings %}" in res:
            p1 = res.split("{% if warnings %}")[0]
            p2 = res.split("{% endif %}")[-2] if len(res.split("{% endif %}")) > 3 else res.split("{% endif %}")[-1]
            if warn_li:
                w_box = f"""<div class="warning-box"><strong>⚠️ Clinical Red Flag Warnings & Allergy Conflicts:</strong><ul style="margin: 5px 0 0 15px; padding: 0;">{warn_li}</ul></div>"""
                res = p1 + w_box + p2

        # Render recommendations box
        rec_li = "".join([f"<li>{r}</li>" for r in context.get("recommendations", [])])
        if "{% if recommendations %}" in res:
            p1 = res.split("{% if recommendations %}")[0]
            p2 = res.split("</body>")[0]
            if rec_li:
                r_box = f"""<div class="recommend-box"><strong>💡 Personalized Health Profile Recommendations:</strong><ul style="margin: 5px 0 0 15px; padding: 0;">{rec_li}</ul></div>"""
                res = p1 + r_box + "</body></html>"

        return res


async def generate_pdf_report(db: Session, doc_id: int) -> str:
    doc = db.query(MedicalDocument).filter(MedicalDocument.id == doc_id).first()
    if not doc:
        raise ValueError(f"Document {doc_id} not found")

    context = build_pdf_context(db, doc_id)
    html_content = render_html_report(context)

    pdf_filename = f"healthai_report_{doc_id}.pdf"
    pdf_filepath = os.path.join(GENERATED_REPORTS_DIR, pdf_filename)

    # 1. Try WeasyPrint if installed
    pdf_generated_success = False
    try:
        from weasyprint import HTML
        HTML(string=html_content).write_pdf(pdf_filepath)
        pdf_generated_success = True
    except Exception as e:
        print(f"[PDFGenerator] WeasyPrint not available or failed: {e}")

    # 2. Try ReportLab / XHTML2PDF fallback
    if not pdf_generated_success:
        try:
            from xhtml2pdf import pisa
            with open(pdf_filepath, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
                if not pisa_status.err:
                    pdf_generated_success = True
        except Exception as e2:
            print(f"[PDFGenerator] xhtml2pdf fallback exception: {e2}")

    # 3. Standard Fallback (Save rendered HTML & text PDF format if no binary engine)
    if not pdf_generated_success:
        html_filepath = os.path.join(GENERATED_REPORTS_DIR, f"healthai_report_{doc_id}.html")
        with open(html_filepath, "w", encoding="utf-8") as hf:
            hf.write(html_content)
        
        with open(pdf_filepath, "w", encoding="utf-8") as pf:
            pf.write(f"%PDF-1.4\n% HealthAI PDF Medical Analysis Report #{doc_id}\n\n" + html_content)
        pdf_generated_success = True

    # Update document record
    doc.pdf_report_path = pdf_filepath
    doc.pdf_generated = 1
    doc.pdf_generated_at = datetime.datetime.utcnow()
    db.commit()

    # Automatically create Timeline Event
    try:
        create_event(
            db=db,
            user_id=doc.user_id,
            event_type="report",
            title="Medical Report PDF Generated",
            summary=f"AI analysis report for '{doc.file_name}' has been converted into a downloadable PDF report.",
            details={
                "document_id": doc.id,
                "file_name": doc.file_name,
                "document_type": doc.document_type,
                "pdf_path": pdf_filepath,
                "generated_at": doc.pdf_generated_at.isoformat()
            }
        )
    except Exception as te:
        print(f"[PDFGenerator] Timeline event creation error: {te}")

    return pdf_filepath
