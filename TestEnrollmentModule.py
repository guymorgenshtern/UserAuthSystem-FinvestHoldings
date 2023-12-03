import unittest
from unittest.mock import Mock, patch
from enrollment_module import EnrollmentModule
from secure_storage import SecureStorage
from subject_enum import Subjects

class TestEnrollmentModule(unittest.TestCase):

    def setUp(self):
        # Mock the SecureStorage and PasswordModule classes since they're not being tested here
        self.mock_secure_storage = Mock(spec=SecureStorage)
        self.mock_password_module = Mock()

        self.enrollment_module = EnrollmentModule(
            secure_storage=self.mock_secure_storage,
            password_module=self.mock_password_module
        )

    def test_enroll_user_success(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'test_user',
            'role': 'C',
            'password': 'StrongP@ssword1',
            'attributes': {'test': 'test'}
        }

        # setting the data for the mock storage to return
        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username does not exist yet
        self.mock_password_module.is_user.return_value = False

        result = self.enrollment_module.enroll_user(token='test_token')

        # enrollment should return true as long as user passes the password check
        self.assertTrue(result)

        # Assert that the add_pass method was called with the correct arguments
        self.mock_password_module.add_pass.assert_called_once_with(
            username='test_user',
            role='C',
            password='StrongP@ssword1',
            attributes={'test': 'test'}
        )

    def test_enroll_user_duplicate_username(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'existing_user',
            'role': 'C',
            'password': 'SecureP@ssword2',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = True

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()

    def test_enroll_user_no_capital(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'non_existing_user',
            'role': 'C',
            'password': 'weakpassword1!',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()

    def test_enroll_user_no_lower(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'non_existing_user',
            'role': 'C',
            'password': 'WEAKPASSWORD1!',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()
    
    def test_enroll_user_no_number(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'non_existing_user',
            'role': 'C',
            'password': 'weakPassword!',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()
    
    def test_enroll_user_no_symbol(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'non_existing_user',
            'role': 'C',
            'password': 'weakPassword1',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()
    
    def test_enroll_user_bad_format(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'non_existing_user',
            'role': 'C',
            'password': '4161111111',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()

    def test_enroll_user_too_short(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'non_existing_user',
            'role': 'C',
            'password': 'W3ak!',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        # since we're mocking the password file, here we are saying that the username already exists
        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()

    def test_enroll_user_same_password_as_username(self):
    # Mock data from the secure storage
        mock_data = {
            'username': 'user',
            'role': 'C',
            'password': 'user',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()
    

    def test_enroll_user_common_password(self):
    # Mock data from the secure storage
        mock_data = {
            'username': 'user',
            'role': 'C',
            'password': 'password',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()

    def test_enroll_user_invalid_username(self):
    # Mock data from the secure storage
        mock_data = {
            'username': 'us:er',
            'role': 'C',
            'password': 'password',
            'attributes': {}
        }

        self.mock_secure_storage.retrieve_secret.return_value = mock_data

        self.mock_password_module.is_user.return_value = False

        # Call the enroll_user method
        result = self.enrollment_module.enroll_user(token='test_token')

        
        self.assertFalse(result)

        # this is an additional check to guarantee that the add_pass method wasn't called since credentials were invalid
        self.mock_password_module.add_pass.assert_not_called()


        
if __name__ == '__main__':
    unittest.main()
