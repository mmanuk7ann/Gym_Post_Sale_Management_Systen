# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from core.config import settings
#
# # Define the configuration for the FastMail client
# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.SMTP_USER,
#     MAIL_PASSWORD=settings.SMTP_PASSWORD,
#     MAIL_FROM=settings.EMAIL_FROM,
#     MAIL_PORT=settings.SMTP_PORT,
#     MAIL_SERVER=settings.SMTP_HOST,
#     MAIL_TLS=settings.EMAIL_TLS,
#     MAIL_SSL=False,  # Disable SSL since TLS is handled
# )
#
# # Initialize FastMail instance
# fast_mail = FastMail(conf)
#
# # Create async function for sending email
# async def send_email(to: str, subject: str, text: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[to],  # List of recipients
#         body=text,
#         subtype="plain"  # Send as plain text
#     )
#     await fast_mail.send_message(message)
