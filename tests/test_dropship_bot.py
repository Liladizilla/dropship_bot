import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("BOT_TOKEN", "test-token")

import dropship_bot


class ProductSearchTests(unittest.TestCase):
    def test_rejects_blank_query(self):
        with self.assertRaisesRegex(ValueError, "product name"):
            dropship_bot.fetch_first_product_url("  ")

    def test_rejects_oversized_query_without_request(self):
        with patch.object(dropship_bot.requests, "get") as get:
            with self.assertRaises(ValueError):
                dropship_bot.fetch_first_product_url("x" * 121)
            get.assert_not_called()

    def test_returns_valid_product_link(self):
        response = Mock()
        response.text = '<a href="/item/123.html">product</a>'
        response.raise_for_status.return_value = None
        with patch.object(dropship_bot.requests, "get", return_value=response):
            self.assertEqual(
                dropship_bot.fetch_first_product_url("phone case"),
                "https://www.aliexpress.com/item/123.html",
            )

    def test_rejects_external_product_like_link(self):
        response = Mock()
        response.text = '<a href="https://evil.example/item/123.html">bad</a>'
        response.raise_for_status.return_value = None
        with patch.object(dropship_bot.requests, "get", return_value=response):
            self.assertIsNone(dropship_bot.fetch_first_product_url("phone case"))

    def test_uses_request_timeout(self):
        response = Mock()
        response.text = ""
        response.raise_for_status.return_value = None
        with patch.object(dropship_bot.requests, "get", return_value=response) as get:
            dropship_bot.fetch_first_product_url("headphones")
            self.assertEqual(get.call_args.kwargs["timeout"], dropship_bot.REQUEST_TIMEOUT_SECONDS)


if __name__ == "__main__":
    unittest.main()
