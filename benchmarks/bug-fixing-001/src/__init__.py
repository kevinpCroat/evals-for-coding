"""
DateRange Utility Library

A simple library for working with date ranges and calculating business days.
"""

from .daterange import (
    get_business_days,
    get_date_range,
    is_business_day,
    count_weekends,
)

__version__ = "1.0.0"
__all__ = [
    "get_business_days",
    "get_date_range",
    "is_business_day",
    "count_weekends",
]
