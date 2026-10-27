"""Public contact / inquiry endpoint (optional SMTP)."""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, HTTPException

from app.core.audit import AuditLogger
from app.core.config import settings
from app.models.schemas import ContactForm

router = APIRouter()
logger = logging.getLogger("goodlife.contact")
_audit = AuditLogger()


def _send_email(form: ContactForm) -> bool:
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD, settings.SMTP_TO]):
        logger.info("SMTP not configured – contact logged only")
        return False
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
    msg["To"] = settings.SMTP_TO
    msg["Subject"] = f"New Inquiry: {form.name} via GoodLife Gateway"
    body = (
        f"Name: {form.name}\n"
        f"Email: {form.email}\n"
        f"Organization: {form.organization or 'N/A'}\n\n"
        f"Message:\n{form.message}\n"
    )
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(msg["From"], settings.SMTP_TO, msg.as_string())
        return True
    except Exception as e:
        logger.error("SMTP send failed: %s", e)
        return False


@router.post("/contact")
async def submit_contact(form: ContactForm):
    """Receive partner / website inquiry. Never logs passwords or secrets."""
    emailed = _send_email(form)
    _audit.log(
        event_type="contact.submit",
        actor=form.email,
        detail={"name": form.name, "organization": form.organization, "emailed": emailed},
    )
    return {
        "status": "SUCCESS",
        "message": "Inquiry securely routed into framework core.",
        "emailed": emailed,
    }
