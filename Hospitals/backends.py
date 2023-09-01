# import logging
# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.hashers import check_password
# from django.utils.encoding import force_bytes

# from Hospitals.models import Hospital

# logger = logging.getLogger(__name__)

# class EmailAuthBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None):
    
#         logger.debug("Authenticating user...")
#         try:
#             hospitals= Hospital.objects.get(email=username)
#             logger.debug(f"Hospital with email {username} found in the database.")
#             if hospitals.check_password(password):
#                 logger.debug("Password found in database. Validating...")
#                 if check_password(password, hospitals.password):
#                     logger.debug("Password is valid. hospitals authenticated successfully.")
#                     return hospitals
#                 else:
#                     logger.warning("Password is invalid. Login failed.")
#             else:
#                 logger.warning("Invalid password. Login failed.")
#         except Hospital.DoesNotExist:
#             logger.warning(f"Hospital with email {username} not found in the database.")

#         return None
    
#     def get_user(self, client_id):
#         try:
#             hospital = Hospital.objects.get(user_id=client_id)
#             logger.debug(f"Hospital with client_id {client_id} found in the database.")
#             return hospital
#         except Hospital.DoesNotExist:
#             logger.warning(f"Hospital with client_id {client_id} not found in the database.")
#             return None
