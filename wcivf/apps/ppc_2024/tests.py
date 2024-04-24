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


class TestPPCFilter(TestCase):
    def test_party_filter(self):
        """Test that the party filter is working
        and returns parties with exact matches"""
        call_command("import_2024_ppcs")
        response = self.client.get("/ppcs/details/")
        self.assertEqual(response.status_code, 200)
        # Check that the filters for both parties are present
        self.assertContains(response, "Independent")
        self.assertContains(response, "Ashfield Independents")

        response = self.client.get("/ppcs/details/?party_name=Independent")
        table = response.context["table"]
        # confirm that the column in the table for "Party" contains only "Independent"
        self.assertEqual(
            [row["Party"] for row in table.data],
            ["Independent"] * len(table.data),
        )
