from dataclasses import dataclass, astuple, asdict
from datetime import datetime
from typing import Optional, Iterable, Any


@dataclass
class TransactionDto:
    date: Optional[str]
    transaction_type: Optional[str]
    num: Optional[str]
    posting: Optional[str]
    name: Optional[str]
    memo_description: Optional[str]
    account: Optional[str]
    split: Optional[str]
    amount: Optional[str]

    @staticmethod
    def from_obj(obj):
        return TransactionDto(
            date=obj.get("Date"),
            transaction_type=obj.get("Transaction Type"),
            num=obj.get("Num"),
            posting=obj.get("Posting"),
            name=obj.get("Name"),
            memo_description=obj.get("Memo/Description"),
            account=obj.get("Account"),
            split=obj.get("Split"),
            amount=obj.get("Amount"),
        )

    def to_obj(self):
        return {
            "Date": self.date,
            "Transaction Type": self.transaction_type,
            "Num": self.num,
            "Posting": self.posting,
            "Name": self.name,
            "Memo/Description": self.memo_description,
            "Account": self.account,
            "Split": self.split,
            "Amount": self.amount,
        }

    # required for dictionary unpacking
    def keys(self) -> Iterable:
        return asdict(self).keys()

    # required for dictionary unpacking
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)
