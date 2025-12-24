from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings

class StaffProfile(models.Model):
    """
    Staff member profile and metadata
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='staff_members')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    display_name = models.CharField(max_length=100)
    POSITION_CHOICES = [
        ('WAITER', 'Waiter'),
        ('BARTENDER', 'Bartender'),
        ('CHEF', 'Chef'),
        ('HOST', 'Host'),
        ('OTHER', 'Other'),
    ]
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'

    def __str__(self):
        return f"{self.display_name} - {self.business.name}"
    
    
    def generate_qr_code(self, shift_id=None):
        """
        Creates a QR token for this staff member.
        
        Generates a unique QR code that customers can scan to tip this staff member.
        If shift_id is provided, associates the QR code with a specific shift.
        
        Args:
            shift_id (int, optional): ID of the shift to associate with the QR code
            
        Returns:
            QRCode: The newly created QR code instance
        """
        pass
    
    def get_tips_total(self, date_range):
        """
        Returns the total sum of tips received for a given time period.
        
        Calculates and aggregates all tips this staff member received within
        the specified date range.
        
        Args:
            date_range (tuple): A tuple of (start_date, end_date) as datetime objects
            
        Returns:
            Decimal: Total tip amount for the period
        """
        pass
    
    def get_active_qr_codes(self):
        """
        Returns all unexpired QR codes for this staff member.
        
        Queries and returns QR codes that are still valid (not expired) and
        associated with this staff profile.
        
        Returns:
            QuerySet: Active QR code instances for this staff member
        """
        pass
    
    def deactivate(self):
        """
        Marks staff member as inactive and invalidates all their QR codes.
        
        Sets is_active to False, records the left_at timestamp, and expires
        all active QR codes associated with this staff member. This is typically
        called when a staff member leaves the business.
        
        Returns:
            None
        """
        pass

class StaffQRCode(models.Model):
    """
    Unique, time-limited QR codes for staff
    """
    
    # QR Type choices
    SHIFT = 'SHIFT'
    DAILY = 'DAILY'
    PERSISTENT = 'PERSISTENT'
    
    QR_TYPE_CHOICES = [
        (SHIFT, 'Shift'),
        (DAILY, 'Daily'),
        (PERSISTENT, 'Persistent'),
    ]
    
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_profile = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, related_name='qr_codes')
    token = models.CharField(max_length=64, unique=True)
    qr_type = models.CharField(max_length=20, choices=QR_TYPE_CHOICES)
    shift_id = models.CharField(max_length=100, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(null=True, blank=True)
    scan_count = models.IntegerField(default=0)
    max_scans = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_scanned_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Staff QR Code'
        verbose_name_plural = 'Staff QR Codes'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['staff_profile']),
            models.Index(fields=['valid_until']),
        ]
    
    def __str__(self):
        return f"QR Code for {self.staff_profile.display_name} - {self.qr_type}"
    
    def validate(self):
        """
        Checks if QR code is valid based on time, scan count, and active status.
        
        Performs validation to determine if this QR code can be used:
        - Checks if is_active is True
        - Verifies current time is between valid_from and valid_until
        - Checks if scan_count hasn't exceeded max_scans (if set)
        
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
                   Returns (True, None) if valid, (False, error_reason) if invalid
        """
        pass
    
    def increment_scan(self):
        """
        Increments the scan count and updates the last_scanned_at timestamp.
        
        Called each time the QR code is successfully scanned. Updates the scan_count
        by 1 and records the current datetime in last_scanned_at. May automatically
        invalidate the QR code if max_scans is reached.
        
        Returns:
            bool: True if increment successful, False if max scans reached
        """
        pass
    
    def invalidate(self):
        """
        Marks the QR code as inactive.
        
        Sets is_active to False, preventing any further use of this QR code.
        This is typically called when a shift ends, staff member leaves, or
        the QR code needs to be revoked for security reasons.
        
        Returns:
            None
        """
        pass
    
    def generate_qr_image(self):
        """
        Creates the actual QR code image (optional).
        
        Generates a scannable QR code image containing the token. The image
        can be saved to a file or returned as a byte stream for display.
        May include branding or styling elements.
        
        Returns:
            BytesIO or str: QR code image as binary stream or file path
        """
        pass