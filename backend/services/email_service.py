import os
import httpx
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "healthai@yourdomain.com")
APP_URL = os.getenv("APP_URL", "http://localhost:3000")

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

def render_template(template_name: str, context: dict) -> str:
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            for key, val in context.items():
                content = content.replace(f"{{{{ {key} }}}}", str(val))
                content = content.replace(f"{{{{{key}}}}}", str(val))
            return content
    return f"<h3>{context.get('title', 'HealthAI Notification')}</h3><p>{context.get('summary', '')}</p>"


async def send_email(to_email: str, subject: str, template_name: str, context: dict) -> bool:
    context["app_url"] = APP_URL
    html_content = render_template(template_name, context)

    # 1. Try Resend HTTP API if configured
    if RESEND_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {RESEND_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from": EMAIL_FROM,
                        "to": [to_email],
                        "subject": subject,
                        "html": html_content
                    }
                )
                if resp.status_code in [200, 201]:
                    return True
                else:
                    print(f"[EmailService] Resend returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[EmailService] Resend exception: {e}")

    # 2. Fallback to standard SMTP if SMTP env configured
    smtp_host = os.getenv("SMTP_HOST")
    if smtp_host:
        try:
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_user = os.getenv("SMTP_USER", "")
            smtp_pass = os.getenv("SMTP_PASS", "")

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = EMAIL_FROM
            msg["To"] = to_email
            msg.attach(MIMEText(html_content, "html"))

            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)
            server.sendmail(EMAIL_FROM, [to_email], msg.as_string())
            server.quit()
            return True
        except Exception as se:
            print(f"[EmailService] SMTP exception: {se}")

    # 3. Development Fallback (Logger output)
    print(f"[EmailService LOG] Simulated Email to {to_email} | Subject: '{subject}'")
    return True
