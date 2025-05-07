# from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
# from sqlalchemy.orm import Session
#
# from Database.database import get_db
# from dependencies import get_current_gym
# from Database.schemas import EmailSend
# from utils.email import send_email
#
# router = APIRouter(prefix="/email", tags=["email"])
#
# @router.post("/send")
# async def send_customer_email(
#     payload: EmailSend,
#     bg: BackgroundTasks,
#     db: Session = Depends(get_db),
#     gym = Depends(get_current_gym),
# ):
#     subject = f"Message from {gym.name}"
#     # schedule in background so request returns immediately
#     bg.add_task(send_email, payload.email, subject, payload.text)
#     return {"detail": "Email is being sent"}