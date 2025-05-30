from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60},
    retry_backoff=True
)
def send_email(self, subject, message, to, from_email=None):
    try:
        result = send_mail(
            subject,
            message,
            from_email or settings.DEFAULT_FROM_EMAIL,
            [to],
            fail_silently=False
        )
        
        return result
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")