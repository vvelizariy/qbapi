from rest_framework import serializers

from transactions.models import Transactions


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["date", "transaction_type", "num", "posting", "name", "memo_description", "account", "split", "amount"]