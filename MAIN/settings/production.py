from .base import *

# Secret key (change this in production, use environment variable)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "sfdfghjklmkmdnu%%vgq123091hokeee~120831-?--/")

# Disable debugging in production
DEBUG = False


ALLOWED_HOSTS = ["your-production-domain.com", "www.your-production-domain.com"]

# Configure your production database here (e.g., PostgreSQL or MySQL)

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "u714077623_HMS_API_TEST",
#         "USER": "u714077623_HMS_API_TEST",
#         "PASSWORD": "n46Q@6&XLh3nd5N",
#         "HOST": "217.21.88.8",  # Change if your MySQL server is running on a different host
#         "PORT": "3306",  # Change if your MySQL server is running on a different port
#     }
# }

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "Debug_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/api.log"),
            "formatter": "verbose",
        },
        "Hospital_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Hospitals.log"),
            "formatter": "verbose",
        },
        "doctor_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/doctors.log"),
            "formatter": "verbose",
        },
        "patient_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/patients.log"),
            "formatter": "verbose",
        },
        "booking_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Appointment.log"),
            "formatter": "verbose",
        },
        "Bed_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Beds.log"),
            "formatter": "verbose",
        },
        "feedbacks_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/feedbacks.log"),
            "formatter": "verbose",
        },
        "Medicines_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Medicines.log"),
            "formatter": "verbose",
        },
        "Nurses_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Nurses.log"),
            "formatter": "verbose",
        },
        "PrescriptionDetails_file": {  # Corrected handler name
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/PrescriptionDetails.log"),
            "formatter": "verbose",
        },
        "Prescriptions_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Prescriptions.log"),
            "formatter": "verbose",
        },
        "LabTest_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/LabTest.log"),
            "formatter": "verbose",
        },
        "Payment_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Payments.log"),
            "formatter": "verbose",
        },
        "Invoice_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/Invoices.log"),
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["Debug_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "Hospitals.Hospital": {
            "handlers": ["Hospital_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "doctors.doctor": {
            "handlers": ["doctor_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "patients.patient": {
            "handlers": ["patient_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Appointments.Appointment": {
            "handlers": ["booking_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Beds.Bed": {
            "handlers": ["Bed_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "feedbacks.feedback": {
            "handlers": ["feedbacks_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Medicines.Medicine": {
            "handlers": ["Medicines_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Nurses.Nurse": {
            "handlers": ["Nurses_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "PrescriptionDetails.PrescriptionDetail": {  # Corrected logger name
            "handlers": ["PrescriptionDetails_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Prescriptions.Prescription": {
            "handlers": ["Prescriptions_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "LabTests.LabTest": {
            "handlers": ["LabTest_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Payments.Payment": {
            "handlers": ["Payment_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "Invoices.Invoice": {
            "handlers": ["Invoice_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


