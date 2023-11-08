from pydantic import EmailStr

from src.config import settings
from src.tasks.email_templates import create_booking_confirmation_template
from src.tasks.manager import celery_app

from pathlib import Path
from PIL import Image
import smtplib


@celery_app.task
def process_pic(
        path: str
        ):
    im_path = Path(path)
    im = Image.open(im_path)
    # im_resized_1000_500 = im.resize((1000, 500))
    # im_resized_200_100 = im.resize((200, 100))
    # im_resized_1000_500.save(f"src/static/images/resized_1000_500_{im_path.name}")
    # im_resized_200_100.save(f"src/static/images/resized_200_100_{im_path.name}")
    im.save(f"src/static/images/test_{im_path.name}")
    return


@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_to_mock = ''
    msg_content = create_booking_confirmation_template(booking, email_to_mock)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
    return
