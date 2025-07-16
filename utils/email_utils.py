import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # you@gmail.com
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # 16-digit App-Password
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # target mailbox

# Check if environment variables are set
if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
    raise ValueError(
        "One or more email environment variables (EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER) are not set."
    )


def send_email(subject: str, body: str) -> None:
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    # SSL from byte 0 – *no* starttls()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        try:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        except smtplib.SMTPAuthenticationError as e:
            raise ValueError(
                "Authentication failed. Check your EMAIL_SENDER and EMAIL_PASSWORD."
            ) from e

        smtp.send_message(msg)
