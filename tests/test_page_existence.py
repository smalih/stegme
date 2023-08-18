import unittest, sys

sys.path.append('..')

from app import app

class PageExistenceTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()


    def test_upload_page(self):
        response = self.app.get('/', follow_redirects=True)
    
    def register(self, email, password, fname, surname):
        x = self.app.post('/register', data=dict(fname=fname, surname=surname, email=email, password=password, confirm=password))
        return x
    
    def login(self, email, password):
        return self.app.post('/login', data=dict(email=email, password=password))
    
    def test_valid_email(self, email='test@test.com', password='testing123', fname='Valid', surname='Email'):
        response = self.register(email, password, fname, surname)
        return self.assertEqual(response.status_code, 200)
    
    # def test_invalid_email1(self, email='test.com', password='testing123', fname='Invalid', surname='Email1'):
    #     response = self.register(email, password, fname, surname)
    #     return self.assertNotEqual(response.status_code, 200)
    
    # def test_invalid_email2(self, email='test@test', password='testing123', fname='Invalid', surname='Email2'):
    #     response = self.register(email, password, fname, surname)
    #     return self.assertNotEqual(response.status_code, 200)
    
if __name__ == '__main__':
    unittest.main()