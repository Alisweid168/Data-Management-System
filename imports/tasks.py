import pandas as pd
from celery import shared_task
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Customer
import logging

logger = logging.getLogger(__name__)

BATCH_SIZE = 10_000  # Adjust batch size as needed


@shared_task
def import_customers(csv_file_path):
    """
    Celery task to efficiently import customer data from an Excel file (100,000+ rows).
    """
    try:
        logger.info("Starting customer import process...")

        df = pd.read_excel(csv_file_path, engine="openpyxl")

        # Clean data
        df.fillna('', inplace=True)
        df['name'] = df['name'].astype(str).str.strip()
        df['email'] = df['email'].astype(str).str.strip()
        df['phone'] = df['phone'].astype(str).str.strip()
        df['address'] = df['address'].astype(str).str.strip()

        # Remove rows with missing required fields
        df = df[(df['name'] != '') & (df['email'] != '')]

        # Get existing emails to prevent duplicates
        existing_emails = set(Customer.objects.values_list('email', flat=True))
        df = df[~df['email'].isin(existing_emails)]

        # Create customer objects
        customers = [
            Customer(
                name=row['name'][:255],
                email=row['email'][:255],
                phone=row['phone'][:15] if row['phone'] else None,
                address=row['address'][:255] if row['address'] else None
            )
            for _, row in df.iterrows()
        ]

        # Bulk insert customers in batches
        total_records = len(customers)
        logger.info(f"Total records to insert: {total_records}")

        created_count = 0
        with transaction.atomic():
            for i in range(0, total_records, BATCH_SIZE):
                batch = customers[i : i + BATCH_SIZE]
                Customer.objects.bulk_create(batch, batch_size=len(batch))
                created_count += len(batch)
                logger.info(f"Inserted {created_count}/{total_records} records...")

        logger.info(f"Import completed: {created_count} records added.")

        send_import_success_email("ali.sweidan003@gmail.com", created_count)
        
        return {"success": created_count, "errors": []}

    except Exception as e:
        logger.error(f"Import failed: {e}")
        return {"success": 0, "errors": [str(e)]}

@shared_task
def send_import_success_email(user_email, record_count):
    """
    Sends a confirmation email after the customer import is successful.
    """
    subject = "Customer Data Import Completed"
    message = f"Your data import has been successfully completed. {record_count} records were added."
    
    from_email = settings.EMAIL_HOST_USER  # Use configured email
    recipient_list = [user_email]  # Send to the provided email

    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"✅ Email sent to {user_email}")
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")