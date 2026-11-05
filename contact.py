from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field
router = APIRouter()
class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=5000)
@router.post("/contact")
async def submit_contact(form: ContactForm):
    return {"status": "SUCCESS", "message": "Inquiry received."}
