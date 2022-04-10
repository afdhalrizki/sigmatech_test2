from django.db import models
from django.conf import settings
import uuid

# Balance
class Balance(models.Model):
    balance_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    balance = models.IntegerField()
    debit = models.IntegerField()
    credit = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=10)

# TopUp
class TopUp(models.Model):
    top_up_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    amount_top_up = models.IntegerField()
    balance_before = models.IntegerField()
    balance_after = models.IntegerField()
    remarks = models.CharField(max_length=240)
    status = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    balance = models.OneToOneField(Balance, on_delete=models.CASCADE)

# Payment
class Payment(models.Model):
    payment_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    amount = models.IntegerField()
    remarks = models.CharField(max_length=240)
    balance_before = models.IntegerField()
    balance_after = models.IntegerField()
    status = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    balance = models.OneToOneField(Balance, on_delete=models.CASCADE)

# Transfer
class Transfer(models.Model):
    transfer_id = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)
    amount = models.IntegerField()
    remarks = models.CharField(max_length=240)
    balance_before = models.IntegerField()
    balance_after = models.IntegerField()
    status = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    balance = models.OneToOneField(Balance, on_delete=models.CASCADE)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)