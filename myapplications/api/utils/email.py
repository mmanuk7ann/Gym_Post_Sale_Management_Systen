# utils/emails.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings

class EmailClient:
    def __init__(self):
        self.server = settings.SMTP_SERVER
        self.port = settings.SMTP_PORT
        self.username = str(settings.SMTP_USERNAME)
        self.password = settings.SMTP_PASSWORD

    def send_email(self, to_email: str, subject: str, body: str) -> None:
        """Compose and send a plain‐text email."""
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.server, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.sendmail(self.username, to_email, msg.as_string())
