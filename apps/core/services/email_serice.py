from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.core.services.base_service import ServiceBase


class EmailService(metaclass=ServiceBase):
    def send_email(self, subject, message, to):
        try:
            result = send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to],
                fail_silently=False
            )
            
            if result == 0:
                raise Exception("Failed to send email")
                
            return True
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")

    def send_invitation_email(self, email, token):
        subject = 'Invitation to join Familiar Hub'
        message = f'Click the link below to join Familiar Hub: {settings.FRONTEND_URL}/register/?token={token}'

        return self.send_email(subject, message, email)