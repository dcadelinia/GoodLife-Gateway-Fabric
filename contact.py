"""Contact / lead form endpoints."""

from __future__ import annotations

import logging

from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr, Field

from app.core.audit import AuditLogger
from app.core.config import settings

logger = logging.getLogger("goodlife.contact")
router = APIRouter()
audit = AuditLogger()


class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=5000)
    organization: str | None = None


@router.post("/contact", status_code=status.HTTP_202_ACCEPTED)
async def submit_contact(form: ContactForm):
    """Accept contact / partnership inquiries (logged; email optional)."""
    audit.log(
        event_type="contact.submitted",
        actor=form.email,
        detail={
            "name": form.name,
            "organization": form.organization,
            "message_len": len(form.message),
        },
    )
    logger.info(
        "Contact form from %s <%s> org=%s",
        form.name,
        form.email,
        form.organization,
    )
    # In production you would enqueue email via SMTP / Resend here.
    # For deployability we only acknowledge receipt.
    return {
        "status": "received",
        "message": "Thank you. Your message has been logged and will be reviewed.",
        "admin": settings.ADMIN_EMAIL,
    }
