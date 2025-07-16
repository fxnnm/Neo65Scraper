import unittest
from unittest.mock import mock_open, patch

from scraper import get_notion_text, load_last_status, save_status


class TestScraper(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="<span>Neo65:</span><span> invoiced on 2024/10/24, not paid </span>",
    )
    def test_get_notion_text(self, mock_file):
        with patch("scraper.BeautifulSoup") as mock_soup:
            mock_soup.return_value.find_all.return_value = [
                MockSpan("Neo65:"),
                MockSpan("invoiced on 2024/10/24, not paid"),
            ]
            result = get_notion_text()
            self.assertEqual(result, "Neo65: invoiced on 2024/10/24, not paid")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Neo65: invoiced on 2024/10/24, not paid",
    )
    def test_load_last_status(self, mock_file):
        result = load_last_status()
        self.assertEqual(result, "Neo65: invoiced on 2024/10/24, not paid")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_status(self, mock_file):
        save_status("Neo65: invoiced on 2024/10/24, not paid")
        mock_file.assert_called_once_with("status.txt", "w")
        mock_file().write.assert_called_once_with(
            "Neo65: invoiced on 2024/10/24, not paid"
        )


class MockSpan:
    def __init__(self, text):
        self.text = text

    def get_text(self):
        return self.text


if __name__ == "__main__":
    unittest.main()
