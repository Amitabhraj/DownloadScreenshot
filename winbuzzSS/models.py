from django.db import models

# Create your models here.
class Deposit_Screenshot(models.Model):
    deposit_type = models.CharField(max_length=100)
    amount = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=120, blank=True, null=True)
    last_4_digit_account_number = models.CharField(max_length=4)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    utr = models.CharField(max_length=12, unique=True)
    trid = models.CharField(max_length=13, unique=True)
    self_account_number = models.CharField(max_length=20)
    screenshot_photo = models.ImageField(blank=True,default=None)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of record creation
    updated_at = models.DateTimeField(auto_now=True)       # Timestamp of last update

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.approved}"
