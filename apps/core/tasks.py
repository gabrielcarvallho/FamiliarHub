import boto3
from botocore.exceptions import ClientError

from celery import shared_task
from django.conf import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 3, 'countdown': 60},
    retry_backoff=True
)
def send_email_aws_ses(self, subject, message, to_addresses):
    client = boto3.client(
        'ses',
        region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    try:
        response = client.send_email(
            Source=settings.DEFAULT_FROM_EMAIL,
            Destination={
                'ToAddresses': [to_addresses],
            },
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': message}},
            },
        )

        return response
    except ClientError as e:
        raise Exception(f"Error sending ses: {e.response['Error']['Message']}")