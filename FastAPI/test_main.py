
import unittest
from unittest.mock import patch, MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

class TestPopulationEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch('main.get_db')
    def test_create_population(self, mock_get_db):

        mock_db_session = MagicMock()
        mock_get_db.return_value = mock_db_session
        
        test_data = [
            {'count': 7, 'expected_status': 200},
            {'count': -5, 'expected_status': 400},
            {'count': "test", 'expected_status': 422}
        ]
        mock_db_session.query().offset().limit().all.return_value = test_data

        #test for invalid input
        for data in test_data:
            response = self.client.post("/population/",json={'count': data['count']})
            self.assertEqual(response.status_code, data['expected_status'])

    @patch('main.get_db')
    def test_retrieve_factorial(self, mock_get_db):

        mock_db_session = MagicMock()
        mock_get_db.return_value = mock_db_session

        test_data = { 'count': 4, 'date': str(datetime.now().replace(microsecond=0)), 'factorial': 24 }
    
        mock_db_session.query().offset().limit().all.return_value = test_data
      
        response = self.client.get("/population/")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_search_population_by_count(self):
        # test valid input
        response = self.client.get("/population/search/?count=3")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))

        # test negative input
        response = self.client.get("/population/search/?count=-100")
        self.assertEqual(response.status_code, 400)
        error_detail = response.json()['detail']
        self.assertEqual(error_detail, "Invalid input. Count cannot be a negative number.")

        # test not found input
        response = self.client.get("/population/search/?count=20")
        self.assertEqual(response.status_code, 404)
        error_detail = response.json()['detail']
        self.assertEqual(error_detail, "Count not found in the database.")

if __name__ == '__main__':
    unittest.main()


