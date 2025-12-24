from django.db import models
import uuid
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Business(models.Model):
    # Represents a hospitality business
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    BUSINESS_TYPE_CHOICES = [
        ('RESTAURANT', 'Restaurant'),
        ('CAFE', 'Cafe'),
        ('BAR', 'Bar'),
        ('HOTEL', 'Hotel'),
        ('OTHER', 'Other'),
    ]
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default="OTHER")
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="business_logos/",
        blank=True,
        null=True
    )
    timezone = models.CharField(max_length=50, default='UTC')
    is_active = models.BooleanField(default=True)
    stripe_account_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # indexes here

    def __str__(self):
        return self.name


    def get_active_locations(self):
        """
        Returns all active locations for this business.
        """
        pass

    def get_total_tips(self, date_range):
        """
        Returns aggregated tips for this business.

        date_range: tuple(start_date, end_date)
        """
        pass

    def add_staff_memeber(self, user, location):
        """
        Creates or reactivates a staff relationship.
        """
        pass

    def remove_staff_member(self, user):
        """
        Deactivates a staff relationship.
        """
        pass


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="Name of the location (e.g., 'Downtown Branch', 'Main Office')")
    address_line1 = models.CharField(max_length=255, verbose_name="Address Line 1")   
    address_line2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, help_text="State, province, or county")
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    country = models.CharField(max_length=2, default='UK', help_text="ISO 3166-1 alpha-2 country code")
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this location is currently active"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # indexes here

    def __str__(self):
        return f"{self.name} - {self.city}"
    
    def get_active_staff(self):
        """
        Returns active staff at this location
        """
        pass

    def get_tips_today(self):
        """
        Returns today's tips for this location
        """
        pass