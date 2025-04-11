"""
Module for sending emails.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail

from app.config import settings

sg_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
template_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class EmailService:
    """Service for sending emails."""

    @staticmethod
    async def is_test_email(email: str) -> bool:
        """Check if the email is a test email."""
        test_domains = {"example.org", "example.com", "test.com", "example.net"}
        domain = email.split("@")[-1]
        return domain in test_domains

    @staticmethod
    async def send_welcome_email(user_email: str, user_name: str):
        """Send a welcome email to a new user."""
        try:
            template = template_env.get_template("auth/welcome.html")
            html_content = template.render(user={"name": user_name})

            message = Mail(
                from_email=From("info@cafesansfil.com"),
                to_emails=user_email,
                subject="Welcome to our service",
                html_content=html_content,
            )
            sg_client.send(message)
        except Exception as e:
            raise Exception(f"Failed to send welcome email: {str(e)}")

    @staticmethod
    async def send_password_reset(user_email: str, reset_link: str):
        """Send a password reset email to a user."""
        try:
            template = template_env.get_template("auth/password_reset.html")
            html_content = template.render(reset_link=reset_link)

            message = Mail(
                from_email=From("info@cafesansfil.com"),
                to_emails=user_email,
                subject="Password Reset Request",
                html_content=html_content,
            )
            sg_client.send(message)
        except Exception as e:
            raise Exception(f"Failed to send password reset email: {str(e)}")

    @staticmethod
    async def send_verification_email(user_email: str, verification_link: str):
        """Send a verification email to a new user."""
        try:
            template = template_env.get_template("auth/verification.html")
            html_content = template.render(verification_link=verification_link)

            message = Mail(
                from_email=From("info@cafesansfil.com"),
                to_emails=user_email,
                subject="Verify your email",
                html_content=html_content,
            )
            sg_client.send(message)
        except Exception as e:
            raise Exception(f"Failed to send verification email: {str(e)}")
