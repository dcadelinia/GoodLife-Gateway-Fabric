from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from app.core.audit import AuditLogger
router = APIRouter()
audit = AuditLogger()

class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=5000)

@router.post("/contact")
async def submit_contact(form: ContactForm):
    audit.log("contact.submission", form.email, {"name": form.name})
    return {"status": "SUCCESS", "message": "Inquiry received."}
