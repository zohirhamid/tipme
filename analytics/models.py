from django.db import models
from django.core.validators import MinValueValidator
import uuid

class TipSummary(models.Model):
    """
    Pre-aggregated daily statistics for performance
    """
    
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name='tip_summaries')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True, related_name='tip_summaries')
    staff_profile = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='tip_summaries')
    date = models.DateField(db_index=True)
    total_tips = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    tip_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='GBP')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tip Summary'
        verbose_name_plural = 'Tip Summaries'
        indexes = [
            models.Index(fields=['business', 'date']),
            models.Index(fields=['staff_profile', 'date']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        if self.staff_profile:
            return f"Tips for {self.staff_profile.display_name} on {self.date}"
        elif self.location:
            return f"Tips for {self.location.name} on {self.date}"
        return f"Tips for {self.business.name} on {self.date}"
    
    def recalculate(self):
        """
        Rebuilds summary from Tip records.
        
        Recalculates the tip statistics by querying all Tip records that match
        the summary's filters (business, location, staff_profile, date):
        - Aggregates total_tips by summing tip amounts
        - Counts tip_count from matching records
        - Only includes tips with payment_status = SUCCEEDED
        - Updates this summary record with fresh calculated values
        - Useful for correcting discrepancies or after refunds
        
        Returns:
            dict: Dictionary containing updated values {'total_tips': Decimal, 'tip_count': int}
        """
        pass