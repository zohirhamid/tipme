from django.db import models
import uuid


class StripeWebhookEvent(models.Model):
    """
    Log Stripe webhook events for debugging and idempotency
    """
    
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=100, db_index=True)
    payload = models.JSONField()
    processed = models.BooleanField(default=False, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Stripe Webhook Event'
        verbose_name_plural = 'Stripe Webhook Events'
        indexes = [
            models.Index(fields=['stripe_event_id']),
            models.Index(fields=['event_type']),
            models.Index(fields=['processed']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.stripe_event_id}"
    
    def process(self):
        """
        Processes the webhook event.
        
        Handles the webhook event based on its event_type:
        - Extracts relevant data from the payload
        - Updates corresponding Tip records (e.g., mark as succeeded/failed)
        - Performs idempotency checks to prevent duplicate processing
        - Handles different event types (payment_intent.succeeded, payment_intent.failed, etc.)
        - Logs any processing errors
        
        Returns:
            tuple: (bool, str) - (success, message)
                   Returns (True, "Success message") if processed successfully,
                   (False, "Error message") if processing fails
        """
        pass
    
    def mark_as_processed(self):
        """
        Updates processed status to True and records processed_at timestamp.
        
        Called after successfully processing the webhook event. Sets processed
        to True and records the current datetime in processed_at. This ensures
        idempotency by preventing the same event from being processed multiple times.
        
        Returns:
            None
        """
        pass