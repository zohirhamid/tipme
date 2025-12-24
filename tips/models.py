from django.db import models

from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Tip(models.Model):
    """
    Immutable tip transaction record
    """
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCEEDED', 'Succeeded'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    staff_profile = models.ForeignKey('StaffProfile', on_delete=models.PROTECT, related_name='tips')
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    currency = models.CharField(max_length=3, default='GBP')
    qr_code = models.ForeignKey('StaffQRCode', on_delete=models.PROTECT, related_name='tips')
    payment_intent_id = models.CharField(max_length=255, unique=True)
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING',
        db_index=True
    )
    idempotency_key = models.CharField(max_length=255, unique=True)
    tip_message = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='tips')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    succeeded_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = 'Tip'
        verbose_name_plural = 'Tips'
        indexes = [
            models.Index(fields=['staff_profile', 'created_at']),
            models.Index(fields=['payment_intent_id']),
            models.Index(fields=['idempotency_key']),
        ]
    
    def __str__(self):
        return f"Tip of {self.currency} {self.amount} to {self.staff_profile.display_name}"
    
    def save(self, *args, **kwargs):
        """
        Override save to enforce immutability rules.
        Only allows updates to payment_status field on existing records.
        """
        if self.pk:  # If this is an update
            original = Tip.objects.get(pk=self.pk)
            # Check if immutable fields have been changed
            immutable_fields = ['amount', 'staff_profile_id', 'payment_intent_id']
            for field in immutable_fields:
                if getattr(self, field) != getattr(original, field):
                    raise ValueError(f"Cannot update immutable field: {field}")
        super().save(*args, **kwargs)
    
    def mark_as_succeeded(self):
        """
        Updates payment_status to SUCCEEDED and records succeeded_at timestamp.
        
        Transitions the tip from PENDING to SUCCEEDED state, recording the exact
        time the payment was confirmed. This should be called when receiving
        webhook confirmation from the payment provider.
        
        Returns:
            bool: True if status updated successfully, False if invalid state transition
        """
        pass
    
    def mark_as_failed(self):
        """
        Updates payment_status to FAILED.
        
        Transitions the tip to FAILED state when payment processing fails.
        Should be called when receiving failure notification from payment provider
        or when payment times out.
        
        Returns:
            bool: True if status updated successfully, False if invalid state transition
        """
        pass
    
    def can_be_refunded(self):
        """
        Checks if tip is refundable based on business logic.
        
        Determines whether this tip is eligible for refund by checking:
        - Payment status is SUCCEEDED
        - Tip is within refund window (e.g., 30 days)
        - No existing refund has been processed
        - Business-specific refund policies
        
        Returns:
            tuple: (bool, str) - (can_refund, reason)
                   Returns (True, None) if refundable, (False, reason) if not
        """
        pass
    
    def create_refund(self):
        """
        Creates a refund record for this tip (if implemented).
        
        Initiates the refund process by:
        - Validating the tip can be refunded via can_be_refunded()
        - Creating a refund transaction with payment provider
        - Creating a Refund model instance (if exists)
        - Updating payment_status to REFUNDED
        
        Returns:
            Refund or None: The created refund instance, or None if refund fails
        """
        pass