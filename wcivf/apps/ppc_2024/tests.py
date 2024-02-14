from django.core.management import call_command
from django.test import TestCase


class TestPPCPersonView(TestCase):
    def test_csv_encoding(self):
        """Test that the CSV is encoded and characters are handled correctly"""
        call_command("import_2024_ppcs")
        response = self.client.get("/ppcs/details/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.charset, "utf-8")
        self.assertContains(response, "Thérèse Côffey")
