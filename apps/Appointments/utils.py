from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import os


# Send Email by Using EmailMessage Class..
class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data["to_email"]],
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send()

    @staticmethod
    def send_doctor_appointment_confirmation(doctor, appointment, patient, client):
        subject = "Appointment Confirmation"
        from_email = os.environ.get("EMAIL_FROM")
        to_email = doctor.email  # Assuming doctor has an email field

        # Create a context dictionary with appointment details and patient details
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
            "to_email": to_email,
            "from_email": from_email,  # Pass the sender email to the send_email method
        }
        Util.send_email(data)

    @staticmethod
    def send_patient_appointment_confirmation(patient, appointment, doctor, client):
        subject = "Appointment Confirmation"
        from_email = os.environ.get("EMAIL_FROM")  # Use the sender email address from settings
        to_email = patient.email  # Assuming patient has an email field

        # Create a context dictionary with appointment details, patient details, and doctor details
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
            "phone": client.phone
        }

        # Render the HTML content using a template (you need to create this template separately)
        html_content = render_to_string("Patient_appointment_confirmation.html", context)

        data = {
            "subject": subject,
            "body": html_content,
            "to_email": to_email,
            "from_email": from_email,  # Pass the sender email to the send_email method
        }
        Util.send_email(data)
