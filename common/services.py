from datetime import datetime
from typing import Dict, List

from common.client import QuickBooksAPIClient
from common.constants import DEFAULT_START_DATE
from common.dto import TransactionDto
from transactions.models import Transactions


class QBTransactionsService:

    def __init__(self):
        self.client = QuickBooksAPIClient()

    def get_transactions(self) -> None:
        """Fetch data from QB API."""
        transactions_data = []
        if latest_transaction := Transactions.objects.all().order_by("-date")[:1]:
            from_date = latest_transaction.get().date
        else:
            from_date = DEFAULT_START_DATE
        to_date = datetime.now().date()
        raw_data_chunks = self.client.retreive_transactions_dataset(from_date=from_date, to_date=to_date)
        for raw_data in raw_data_chunks:
            transactions_data.extend(self._transform_response(data=raw_data))
        self.save_to_db(transactions_data)

    def _transform_response(self, data: Dict) -> List:
        """Transform response to list of key values."""
        transformed_data = []
        col_to_title_mapping = {index: key["ColTitle"] for index, key in enumerate(data["Columns"]["Column"])}
        if data["Rows"]:
            for row in data["Rows"]["Row"]:
                transaction_obj = {col_to_title_mapping[index]:value["value"] for index, value in enumerate(row["ColData"])}
                transformed_data.append(transaction_obj)

        return transformed_data

    def save_to_db(self, transactions):
        """Save transactions to db."""
        for transaction in transactions:
            record = TransactionDto.from_obj(transaction)
            Transactions.objects.create(**record)
