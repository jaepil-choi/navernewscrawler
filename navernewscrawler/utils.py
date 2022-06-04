from typing import Any, Dict, List, Optional, Union

import pandas as pd
import numpy as np

from pathlib import Path

import itertools
import datetime

HEADERS = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "referer": u,
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            }

CWD = Path('.').resolve()
BASE_DIR = CWD / 'cache' / 'navernews'

## directory generation 
def generate_dirs(self, security_code, frequency="month"):

    # freq_dtype = CacheSaver.frequency2dtype[frequency] # TODO: Dynamically change directory structure based on frequency parameter
    years = DateUtil.inclusive_daterange(self.min_date, self.max_date, "year")
    years = [DateUtil.npdate2str(y)['year'] for y in years]
    months = DateUtil.inclusive_daterange(self.min_date, self.max_date, "month")
    months = [DateUtil.npdate2str(m)['month'] for m in months]

    p = BASE_DIR / security_code
    
    for year, month in itertools.product(years, months):
        (p / year / month).mkdir(parents=True, exist_ok=True)



## Util codebase copied from korquanttools
class DateUtil:
    @staticmethod
    def validate_date(yyyymmdd: Union[str, int], start="19900101", end="21000101") -> bool:
        """Check wheter the given input has valid date format & value regardless of type

        Args:
            yyyymmdd (Union[str, int]): date format in yyyymmdd, i.e: %Y%m%d
            start (str, optional): Start date of sanity check. Defaults to "19900101".
            end (str, optional): End date of sanity check. Defaults to "21000101".

        Returns:
            bool: True if the input has a valid date format & value. 
        """        

        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)

        if isinstance(yyyymmdd, (str, int)):
            date = str(yyyymmdd)

            try:
                date = pd.to_datetime(yyyymmdd)
                return (start_date < date < end_date)
            except:
                return False
        
        if isinstance(yyyymmdd, datetime.datetime) or isinstance(yyyymmdd, np.datetime64):
            try:
                date = pd.to_datetime(yyyymmdd)
                return (start_date < date < end_date)
            except:
                return False
        else:
            return False

    @staticmethod
    def validate_date2str(yyyymmdd: Union[str, int]) -> str:
        if DateUtil.validate_date(yyyymmdd):
            return str(yyyymmdd)
        else:
            raise Exception(f"Date validation failed. Given: yyyymmdd = {yyyymmdd}")

    @staticmethod
    def validate_date2int(yyyymmdd: Union[str, int]) -> int:
        if DateUtil.validate_date(yyyymmdd):
            return int(yyyymmdd)
        else:
            raise Exception(f"Date validation failed. Given: yyyymmdd = {yyyymmdd}")
    
    @staticmethod
    def intDate_2_timestamp(yyyymmdd: int):
        date = str(yyyymmdd)
        return pd.to_datetime(date, format="%Y%m%d")
    
    @staticmethod
    def timestamp_2_intDate(timestamp, format="%Y%m%d"):
        date = timestamp.strftime(format=format)
        return int(date)
    
    @staticmethod
    def inclusive_daterange(start_date, end_date, frequency):
        # TODO: Maybe just use pd.date_range in the future, but the problem is that it's not inclusive.
        frequencies = ["day", "month", "year"]
        frequency2dtype = {
        'day': 'datetime64[D]',
        'month': 'datetime64[M]',
        'year': 'datetime64[Y]',
        }
        assert frequency in frequencies

        date_range = np.arange(start_date, end_date + pd.Timedelta(days=1), dtype="datetime64[D]")
        date_range = np.unique(date_range.astype(frequency2dtype[frequency]))

        return date_range

    @staticmethod
    def npdate2str(npdate):
        npdate = npdate.astype("datetime64[D]")
        year, month, date = npdate.astype(str).split('-')
        
        return {'year': year, 'month': month, 'date': date}
    
    @staticmethod
    def numdate2stddate(numdate):
        numdate = str(numdate)
        return numdate[:4] + '-' + numdate[4:6] + '-' + numdate[6:]