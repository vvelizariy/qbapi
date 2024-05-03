import csv

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from common.services import QBTransactionsService
from transactions.models import Transactions
from transactions.serializers import TransactionSerializer


FILENAME_PREFIX = "transactions"


class ListTransactions(ListAPIView):
    """
    Fetch transactions as csv. When user query's it, will be generated csv for specified time range.
    """
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        """
        Return a list of all transactions.
        """
        # This should be done py scheduled task
        QBTransactionsService().get_transactions()

        filename = FILENAME_PREFIX
        columns = [field.name for field in Transactions._meta.get_fields()]
        transactions = Transactions.objects.all()
        if from_date := request.query_params.get("from_date"):
            filename += f"-{from_date}"
            transactions = transactions.filter(date__gt=from_date)
        if to_date := request.query_params.get("to_date"):
            filename += f"-{to_date}"
            transactions = transactions.filter(date__lt=to_date)
        response = HttpResponse(
            content_type="text/csv",
            headers={f"Content-Disposition": f'attachment; filename="{filename}.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(columns)
        for transaction in transactions.values_list(*columns):
            writer.writerow(transaction)

        return response
