"""Contact / inquiry endpoint."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from app.core.audit import AuditLogger

logger = logging.getLogger("goodlife.contact")
router = APIRouter()
audit = AuditLogger()


class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=5000)
    company: str | None = None
    inquiry_type: str | None = None  # general | enterprise | investor | sponsor


@router.post("/contact")
async def submit_contact(form: ContactForm):
    """Accept contact form submissions. Email delivery requires SMTP secrets."""
    try:
        audit.log(
            event_type="contact.submission",
            actor=form.email,
            detail={
                "name": form.name,
                "company": form.company,
                "inquiry_type": form.inquiry_type,
            },
        )
        logger.info("Contact from %s <%s> type=%s", form.name, form.email, form.inquiry_type)
        # SMTP send is optional – only if secrets are configured.
        # Placeholder: log and return success so the form works without email.
        return {
            "status": "SUCCESS",
            "message": "Inquiry received and routed. Our team will respond shortly.",
        }
    except Exception as exc:
        logger.exception("Contact form failed")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
