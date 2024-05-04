import logging
import concurrent.futures
from datetime import date
from typing import Dict, List

import requests
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError

from common.exceptions import QBAPIException
from common.utils import split_date_range_by_months
from quickBooksApi import settings


logger = logging.getLogger(__name__)


class QuickBooksAPIClient:
    """QB OAuth API client."""

    def __init__(self):
        self.auth_client = AuthClient(
            settings.CLIENT_ID,
            settings.CLIENT_SECRET,
            settings.REDIRECT_URI,
            settings.ENVIRONMENT,
            access_token=settings.QB_ACCESS_TOKEN,
            refresh_token=settings.QB_REFRESH_TOKEN,
        )
        try:
            self.auth_client.refresh()
        except AuthClientError as e:
            logger.error(f"Failed to refresh token with status code {e.status_code} tid {e.intuit_tid}")
        except Exception as e:
            logger.error(f"Failed to refresh token with error {e}")

    def retrieve_transactions_dataset(self, from_date: date, to_date: date) -> List[Dict]:
        """
        Split date range to monthly chunks and load data.
        As API has max limit 400000 cells, in transactions case it will be 44_444 transactions, so months is ok,
        anyway on sandbox there are only ~189 transactions.
        """
        result = []
        date_ranges = split_date_range_by_months(from_date, to_date)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_transactions = {executor.submit(self.fetch_transactions, from_date, to_date): to_date for from_date, to_date in date_ranges}
            for future in concurrent.futures.as_completed(future_to_transactions):
                transactions = future_to_transactions[future]
                try:
                    data = future.result()
                    result.append(data)
                except QBAPIException as qb_exc:
                    logger.error(f"{transactions} while fetching data from QB API: {exc}")
                except Exception as exc:
                    logger.error(f"{transactions} generated an exception: {exc}")
                else:
                    logger.error(f"Chunk has {len(data.get("Rows", {}))} records")
        return result

    def fetch_transactions(self, from_date: str, to_date: str) -> Dict:
        """
         Perform plain http request to QB API.
        """
        url = '{0}/v3/company/{1}/reports/TransactionList?start_date={2}&end_date={3}'.format(
            settings.QB_BASE_SANDBOX, settings.REALM_ID, from_date, to_date
        )
        auth_header = 'Bearer {0}'.format(self.auth_client.access_token)
        headers = {
            'Authorization': auth_header,
            'Accept': 'application/json'
        }
        try:
            response = requests.get(url, headers=headers).json()
        except requests.RequestException as exc:
            raise QBAPIException(exc)
        return response

    def _generate_oauth_link(self):
        """
        This method is not used in code, but is handy for initial getting of auth code
        which will be exchanged for access and refresh tokens.
        """
        url = self.auth_client.get_authorization_url([Scopes.ACCOUNTING])
        return url
