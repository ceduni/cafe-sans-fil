# from app.core.config import settings
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# """
# This module is used to send emails to users. (Disable email sending because of Render blocking SMTP requests)
# """

# conf = ConnectionConfig(
#         MAIL_USERNAME=settings.MAIL_USERNAME,
#         MAIL_PASSWORD=settings.MAIL_PASSWORD,
#         MAIL_FROM=settings.MAIL_FROM,
#         MAIL_PORT=settings.MAIL_PORT,
#         MAIL_SERVER=settings.MAIL_SERVER,
#         MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
#         MAIL_STARTTLS=True,
#         MAIL_SSL_TLS=False,
#         USE_CREDENTIALS = True,
#         VALIDATE_CERTS = True,
#         TEMPLATE_FOLDER="utils/templates"
#     )

# async def send_registration_mail(subject: str, email_to: str, body: dict):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         template_body=body,
#         subtype='html',
#     )
    
#     fm = FastMail(conf)
#     await fm.send_message(message, template_name='register_mail.html')

# async def send_reset_password_mail(subject: str, email_to: str, body: dict):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         template_body=body,
#         subtype='html',
#     )
    
#     fm = FastMail(conf)
#     await fm.send_message(message, template_name='reset_password_mail.html')


# async def is_test_email(email: str) -> bool:
#     # To not send emails to test domains in Unit Tests
#     test_domains = {"example.org", "example.com", "test.com", "example.net", "umontreal.ca"}
#     domain = email.split('@')[-1]
#     return domain in test_domains