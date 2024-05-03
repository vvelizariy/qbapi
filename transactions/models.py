from django.db import models


class Transactions(models.Model):
    date = models.DateField()
    transaction_type = models.CharField(max_length=255)
    num = models.CharField(max_length=255)
    posting = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    memo_description = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    split = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date}-{self.amount}"
