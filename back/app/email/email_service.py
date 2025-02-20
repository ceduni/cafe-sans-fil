from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import settings


class EmailRequest(BaseModel):
    from_email: EmailStr
    to_email: EmailStr
    subject: str
    html_content: str


@app.post("/send-email/")
async def send_email(email_request: EmailRequest):
    message = Mail(
        from_email=email_request.from_email,
        to_emails=email_request.to_email,
        subject=email_request.subject,
        html_content=email_request.html_content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return {
            "status_code": response.status_code,
            "body": response.body.decode("utf-8") if response.body else "",
            "headers": dict(response.headers),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# NOT FOR PRODUCTION
###############################################################################
# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='info@cafesansfil.com',
#     to_emails='louis.edouard.lafontant@umontreal.ca',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)
