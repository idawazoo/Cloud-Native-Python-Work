from app9 import app
import unittest

class FlaskappTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def test_tweets_status_code(self): 
        # sends HTTP GET request to the application 
        result = self.app.get('/api/v2/tweets')
        print(result)

        # assert the status code of the response 
        self.assertEqual(result.status_code, 200) 
