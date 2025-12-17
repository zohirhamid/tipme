import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(blank=True)
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('STAFF', 'Staff')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="STAFF")
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def send_verification_email(self):
        # Sends email verification
        pass
    
    def verify_email(self, token):
        # validates and marks emails as verified
        pass

    def has_business_access(self, business_id):
        # Checks ownership or staff relationship
        pass

