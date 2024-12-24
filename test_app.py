import unittest
from app import app  # Import your Flask app


class TestLeaseManagementAPI(unittest.TestCase):

    def setUp(self):
        """Setup the test client."""
        # Create a test client for our Flask app
        self.app = app.test_client()
        self.app.testing = True  # Set the testing flag to true

    def test_top_vacancies(self):
        """Test the '/analytics/top-vacancies' endpoint."""
        response = self.app.get("/analytics/top-vacancies")

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check if the response contains expected JSON structure
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("unit_id", data[0])
        self.assertIn("vacancy_days", data[0])

    def test_leases_ending_soon(self):
        """Test the '/leases/ending-soon' endpoint."""
        # Test with the default 'days' parameter (30 days)
        response = self.app.get("/leases/ending-soon")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Test with custom 'days' parameter (15 days)
        response = self.app.get("/leases/ending-soon?days=15")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_invalid_endpoint(self):
        """Test for an invalid endpoint."""
        response = self.app.get("/invalid-endpoint")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
