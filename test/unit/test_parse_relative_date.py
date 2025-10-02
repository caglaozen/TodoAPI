import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

sys.modules["google"] = MagicMock()
sys.modules["google.adk"] = MagicMock()
sys.modules["google.adk.agents"] = MagicMock()

from src.agent import todo_tools


class TestParseRelativeDate(unittest.TestCase):
    def test_parse_today_english(self):
        """Test parsing 'today' in English."""
        result = todo_tools.parse_relative_date("today")
        expected = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_today_turkish(self):
        """Test parsing 'bugün' in Turkish."""
        result = todo_tools.parse_relative_date("bugün")
        expected = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_tomorrow_english(self):
        """Test parsing 'tomorrow' in English."""
        result = todo_tools.parse_relative_date("tomorrow")
        expected = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_tomorrow_turkish(self):
        """Test parsing 'yarın' in Turkish."""
        result = todo_tools.parse_relative_date("yarın")
        expected = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_next_week_english(self):
        """Test parsing 'next week' in English."""
        result = todo_tools.parse_relative_date("next week")
        expected = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_next_week_turkish(self):
        """Test parsing 'gelecek hafta' in Turkish."""
        result = todo_tools.parse_relative_date("gelecek hafta")
        expected = (datetime.now() + timedelta(weeks=1)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_this_weekend_english(self):
        """Test parsing 'this weekend' in English."""
        result = todo_tools.parse_relative_date("this weekend")
        today = datetime.now()
        days_until_saturday = (5 - today.weekday()) % 7
        expected = (today + timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_this_weekend_turkish(self):
        """Test parsing 'bu hafta sonu' in Turkish."""
        result = todo_tools.parse_relative_date("bu hafta sonu")
        today = datetime.now()
        days_until_saturday = (5 - today.weekday()) % 7
        expected = (today + timedelta(days=days_until_saturday)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)

    def test_parse_valid_date_format(self):
        """Test parsing a valid YYYY-MM-DD format."""
        result = todo_tools.parse_relative_date("2025-12-25")
        self.assertEqual(result, "2025-12-25")

    def test_parse_invalid_date_defaults_to_next_week(self):
        """Test parsing an invalid date defaults to next week."""
        result = todo_tools.parse_relative_date("invalid date")
        expected = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.assertEqual(result, expected)
