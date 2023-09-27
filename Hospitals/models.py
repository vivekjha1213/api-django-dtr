from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        # Create a Hospital instance
        hospital = self.model(email=email, name=name, **extra_fields)
        hospital.set_password(password)
        hospital.save(using=self._db)
        return hospital

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)  # Correct the key name
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_admin') is not True:  # Correct the field name here
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(email, name, password, **extra_fields)


# custom usermodel..
class Hospital(AbstractBaseUser):
    USER_TYPES = [
        ("Admin", "admin"),
        ("Doctor", "doctor"),
        ("Nurse", "nurse"),
        ("Receptionist", "receptionist"),
    ]
    client_id = models.CharField(primary_key=True, max_length=10)
    hospital_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)  # -> this is superuser filed/....
    owner_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)  # Changed to EmailField
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
    )

    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    profile_image = models.ImageField(upload_to="user_profiles/", null=True, blank=True)
    user_logo = models.ImageField(upload_to="user_logos/", null=True, blank=True)

    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # Use this for superuser status

    access_token = models.CharField(max_length=1000, blank=True)
    refresh_token = models.CharField(max_length=1000, blank=True)
    
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()
    
 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]
    
    
    # to ensure unique entries based on 'email' and 'user_type'
    class Meta:  
        unique_together = ('email', 'user_type')  

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        #  "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        #  "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self.is_admin = value


def generate_client_id():
    last_hospital = Hospital.objects.order_by("client_id").last()
    if last_hospital:
        last_id = int(last_hospital.client_id[3:])
        new_id = last_id + 1
    else:
        new_id = 1
    return f"HID{new_id:05}"


@receiver(pre_save, sender=Hospital)
def set_hospital_id(sender, instance, **kwargs):
    if not instance.client_id:
        instance.client_id = generate_client_id()
