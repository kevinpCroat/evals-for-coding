"""
Comprehensive test suite for the daterange library.
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from daterange import (
    is_business_day,
    get_date_range,
    count_weekends,
    get_business_days,
)


class TestIsBusinessDay:
    """Tests for is_business_day function."""

    def test_monday_is_business_day(self):
        # 2025-01-06 is a Monday
        date = datetime(2025, 1, 6)
        assert is_business_day(date) is True

    def test_friday_is_business_day(self):
        # 2025-01-10 is a Friday
        date = datetime(2025, 1, 10)
        assert is_business_day(date) is True

    def test_saturday_is_not_business_day(self):
        # 2025-01-11 is a Saturday
        date = datetime(2025, 1, 11)
        assert is_business_day(date) is False

    def test_sunday_is_not_business_day(self):
        # 2025-01-12 is a Sunday
        date = datetime(2025, 1, 12)
        assert is_business_day(date) is False


class TestGetDateRange:
    """Tests for get_date_range function."""

    def test_single_day_range(self):
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 1)
        result = get_date_range(start, end)
        assert len(result) == 1
        assert result[0] == start

    def test_one_week_range(self):
        start = datetime(2025, 1, 1)
        end = datetime(2025, 1, 7)
        result = get_date_range(start, end)
        assert len(result) == 7

    def test_invalid_range_raises_error(self):
        start = datetime(2025, 1, 10)
        end = datetime(2025, 1, 1)
        with pytest.raises(ValueError):
            get_date_range(start, end)


class TestCountWeekends:
    """Tests for count_weekends function."""

    def test_week_with_one_weekend(self):
        # Monday to Sunday includes 1 weekend (Sat + Sun = 2 days)
        start = datetime(2025, 1, 6)  # Monday
        end = datetime(2025, 1, 12)  # Sunday
        assert count_weekends(start, end) == 2

    def test_weekdays_only_no_weekend(self):
        # Monday to Friday
        start = datetime(2025, 1, 6)  # Monday
        end = datetime(2025, 1, 10)  # Friday
        assert count_weekends(start, end) == 0

    def test_weekend_only(self):
        # Saturday to Sunday
        start = datetime(2025, 1, 11)  # Saturday
        end = datetime(2025, 1, 12)  # Sunday
        assert count_weekends(start, end) == 2


class TestGetBusinessDays:
    """Tests for get_business_days function."""

    def test_single_weekend_day(self):
        # Saturday only - range where start == end
        start = datetime(2025, 1, 11)
        end = datetime(2025, 1, 11)
        # Bug doesn't affect this since start == end means 0 iterations either way
        assert get_business_days(start, end) == 0

    def test_monday_to_saturday(self):
        # Monday to Saturday (ends on weekend)
        start = datetime(2025, 1, 6)  # Monday
        end = datetime(2025, 1, 11)  # Saturday
        # Ends on Saturday, so bug doesn't affect count (loop stops at Friday)
        # Counts Mon-Fri = 5 business days
        assert get_business_days(start, end) == 5

    def test_business_days_one_week_span(self):
        """
        This test covers the edge case where the end date is a Friday (business day).
        Monday to Friday inclusive should be 5 business days.
        This test FAILS due to an off-by-one error in the implementation.

        The bug uses < instead of <= in the loop condition, causing it to exclude
        the end_date from the count. So Monday-Friday returns 4 instead of 5.
        """
        # 2025-01-06 (Monday) to 2025-01-10 (Friday) = 5 days inclusive
        # Business days: Mon(6), Tue(7), Wed(8), Thu(9), Fri(10) = 5 days
        # Bug: counts only Mon-Thu (< not <=), giving 4 business days instead of 5
        start = datetime(2025, 1, 6)  # Monday
        end = datetime(2025, 1, 10)  # Friday
        assert get_business_days(start, end) == 5

    def test_two_week_span(self):
        # Two weeks Mon-Sun (ends on Sunday, so bug doesn't affect it)
        start = datetime(2025, 1, 6)  # Monday
        end = datetime(2025, 1, 19)  # Sunday (2 weeks later)
        # Ends on Sunday (weekend), so the < vs <= doesn't matter
        # Result is 10 business days either way
        assert get_business_days(start, end) == 10

    def test_partial_week(self):
        # Monday to Sunday (ends on weekend)
        start = datetime(2025, 1, 6)  # Monday
        end = datetime(2025, 1, 12)  # Sunday
        # Ends on Sunday, so bug doesn't affect it
        # Counts Mon-Fri = 5 business days
        assert get_business_days(start, end) == 5

    def test_weekend_to_weekend(self):
        # Saturday to Sunday (only weekend days)
        start = datetime(2025, 1, 11)  # Saturday
        end = datetime(2025, 1, 12)  # Sunday
        # No business days in this range
        assert get_business_days(start, end) == 0

    def test_invalid_range_raises_error(self):
        start = datetime(2025, 1, 10)
        end = datetime(2025, 1, 1)
        with pytest.raises(ValueError):
            get_business_days(start, end)

    def test_month_span_ending_on_weekend(self):
        # January 1-12, 2025 (Wed to Sun)
        start = datetime(2025, 1, 1)  # Wednesday
        end = datetime(2025, 1, 12)  # Sunday
        # Ends on Sunday, so bug doesn't affect it
        # Jan 2025: 1(Wed), 2(Thu), 3(Fri), 6(Mon), 7(Tue), 8(Wed), 9(Thu), 10(Fri) = 8 business days
        assert get_business_days(start, end) == 8
