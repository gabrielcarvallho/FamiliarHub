from django.conf import settings

from apps.core.tasks import send_email_aws_ses
from apps.core.services.base_service import ServiceBase


class EmailService(metaclass=ServiceBase):
    def send_invitation_email(self, email, token):
        subject = 'Invitation to join Familiar Hub'
        message = f'Click the link below to join Familiar Hub: {settings.FRONTEND_URL}/register?token={token}'

        result = send_email_aws_ses.delay(subject, message, email)

        if result == 0:
            raise Exception('Failed to send email.')