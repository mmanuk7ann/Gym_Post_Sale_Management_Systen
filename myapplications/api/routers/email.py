from fastapi import APIRouter, HTTPException
import smtplib

from Database.schemas import EmailSend
from utils.email import EmailClient

router = APIRouter(prefix="/email", tags=["email"])

@router.post("/send", summary="Send a plain‐text email")
async def send_customer_email(request: EmailSend):
    client = EmailClient()
    try:
        client.send_email(
            to_email=request.email,
            subject=request.subject_text,
            body=request.text
        )
        return {"detail": "Email sent successfully"}
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="SMTP authentication failed")
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=502, detail=f"SMTP error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")