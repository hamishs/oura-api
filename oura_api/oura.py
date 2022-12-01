import re
import requests
from functools import partialmethod
from typing import Any, Dict, Type, List

from oura_api.exceptions import (
    QueryParameterValidationError, 
    MinimumAppVersionError,
    RequestRateLimitExceeded,
    InternalServerError,
)

class ApiFactory(type):
    """Metaclass to make methods from a template."""
        
    def __new__(cls: Type, clsname: str, bases: List[Type], attrs: Dict[str, Any]):
        for method in attrs["_date_range_methods"]:
            attrs[f"get_{method}"] = partialmethod(
                attrs["_get_data_in_dates"],
                method,
            )
        return super().__new__(cls, clsname, bases, attrs)


class OuraApi(metaclass=ApiFactory):
    """Download data from the Oura Ring API."""

    URL = "https://api.ouraring.com/v2/usercollection/"

    _date_regex = re.compile("\d{4}-\d{2}-\d{2}")
    _datetime_regex = re.compile("\d{4}-\d{2}-\d{2}")

    _date_range_methods = [
        "daily_activity",
        "daily_readiness",
        "daily_sleep",
        "session",
        "sleep",
        "tag",
        "workout",
        "personal_info",
    ]

    def __init__(self, key: str):
        self.key = key
        self.key_header = {"Authorization" : f"Bearer {self.key}"}
        
    def get_heart_rate(self, start_datetime: str, end_datetime: str) -> Dict:
        """Get heart rate within datetime range."""
        response = requests.request(
            "GET",
            self.URL + "heartrate",
            headers=self.key_header,
            params={
                "start_datetime" : start_datetime,
                "end_datetime" : end_datetime,
            }
        )
        self._handle_response(response)
        return response.json()
    
    def _handle_response(self, r: requests.Response) -> None:
        """Check the response."""
        if 200 <= r.status_code <= 299:
            return
        elif r.status_code == 400:
            raise QueryParameterValidationError(QueryParameterValidationError.msg)
        elif r.status_code == 426:
            raise MinimumAppVersionError(MinimumAppVersionError.msg)
        elif r.status_code == 429:
            raise RequestRateLimitExceeded(RequestRateLimitExceeded.msg)
        elif 500 <= r.status_code:
            raise InternalServerError(InternalServerError.msg)
    
    def _get_data_in_dates(self, name: str, start: str, end: str) -> Dict:
        """Get a data value with given date ranges."""
        if len(start) != 10 or self._date_regex.match(start) is None:
            raise ValueError("Start date is not in YYY-MM-DD format.")
        if len(end) != 10 or self._date_regex.match(end) is None:
            raise ValueError("End date is not in YYY-MM-DD format.")
        response = requests.request(
            "GET",
            self.URL + name,
            headers=self.key_header,
            params={
                "start_date" : start,
                "end_date" : end,
            }
        )
        try:
            self._handle_response(response)
        except Exception as e:
            print(f"Exception during data range method: {name}.")
            raise e
        return response.json()
