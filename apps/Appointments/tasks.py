from MAIN.settings.celery import app as celery_app
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import os

from doctors.models import Doctor

@shared_task
def send_email_task(subject, body, from_email, to_email):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=[to_email],
    )
    email.content_subtype = "html"  # Set content type to HTML
    email.send()


@shared_task
def send_doctor_appointment_confirmation(doctor_id, appointment, patient, client):
    subject = "Appointment Confirmation"
    from_email = os.environ.get("EMAIL_FROM")
    
    # Retrieve the doctor object from the doctor_id
    doctor = Doctor.objects.get(doctor_id=doctor_id)

    context = {
        "full_name": f"{doctor.first_name} {doctor.last_name}",
        "appointment_date": appointment.appointment_date.strftime("%Y-%m-%d"),
        "appointment_time": f"{appointment.start_time.strftime('%H:%M')} - {appointment.end_time.strftime('%H:%M')}",
        "patient_name": f"{patient.first_name} {patient.last_name}",
        "patient_email": patient.email,
        "patient_contact_number": patient.contact_number,
        "address": client.address,
    }

    html_content = render_to_string("Doctor_appointment_confirmation.html", context)
    data = {
        "subject": subject,
        "body": html_content,
        "from_email": from_email,
        "to_email": doctor.email,
    }
    send_email_task.delay(**data)


@shared_task
def send_patient_appointment_confirmation(patient, appointment, doctor, client):
    subject = "Appointment Confirmation"
    from_email = os.environ.get("EMAIL_FROM")
    to_email = patient.email

    context = {
        "full_name": f"{patient.first_name} {patient.last_name}",
        "appointment_date": appointment.appointment_date.strftime("%Y-%m-%d"),
        "start_time": appointment.start_time.strftime("%H:%M"),
        "end_time": appointment.end_time.strftime("%H:%M"),
        "hospital_name": client.hospital_name,
        "doctor_name": f"{doctor.first_name} {doctor.last_name}",
        "doctor_specialty": doctor.specialty,
        "doctor_email": doctor.email,
        "doctor_contact_number": doctor.contact_number,
        "address": client.address,
        "phone": client.phone,
    }

    html_content = render_to_string("Patient_appointment_confirmation.html", context)
    data = {
        "subject": subject,
        "body": html_content,
        "from_email": from_email,
        "to_email": to_email,
    }
    send_email_task.delay(**data)
