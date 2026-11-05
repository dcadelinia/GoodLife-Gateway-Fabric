"""Contact / inquiry endpoint. No hardcoded credentials."""
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
    inquiry_type: str | None = None

@router.post("/contact")
async def submit_contact(form: ContactForm):
    try:
        audit.log(event_type="contact.submission", actor=form.email, detail={"name": form.name, "type": form.inquiry_type})
        logger.info("Contact from %s <%s>", form.name, form.email)
        return {"status": "SUCCESS", "message": "Inquiry received. Our team will respond shortly."}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
