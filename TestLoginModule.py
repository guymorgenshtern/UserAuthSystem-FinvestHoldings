import unittest
from unittest.mock import Mock, patch
from login_module import LoginModule
from secure_storage import SecureStorage
from password_module import PasswordModule
from user import User

class TestLoginModule(unittest.TestCase):

    def setUp(self):
        #mock the SecureStorage and PasswordModule classes
        self.mock_secure_storage = Mock(spec=SecureStorage)
        self.mock_password_module = Mock(spec=PasswordModule)

        self.login_module = LoginModule(
            storage=self.mock_secure_storage,
            password_module=self.mock_password_module
        )

    def test_login_success(self):
        # Mock data from the secure storage, this one will have no issues
        mock_data = {
            'username': 'test_user',
            'role': 'C',
            'password': 'StrongP@ssword1',
            'attributes': {'test': 'test'}
        }

        #not testing hashing here so password can just be plaintext, since using Mock I can just set data based on behaviour testing
        self.mock_secure_storage.retrieve_secret.return_value = mock_data['password']

        #Set the return value for the is_user method (user exists)
        self.mock_password_module.is_user.return_value = True

        # Set the return value for the get_user method, should return back everything about the user except password in a User obj
        self.mock_password_module.get_user.return_value = User(mock_data['username'], mock_data['role'], mock_data['attributes'])

        result = self.login_module.login(uid='test_user', token='test_token')

        #assert all attributes are accurate
        self.assertEqual(result.username, 'test_user')
        self.assertEqual(result.role, 'C')

        # User obj appends role as an attribute, gotta do that here too for testing
        attributes_to_check = {'test': 'test'}
        attributes_to_check.update({'role': mock_data['role']})
        self.assertEqual(result.attributes, attributes_to_check)

    def test_login_user_not_exist(self):
        # Set the return value for the is_user method (user does not exist)
        self.mock_password_module.is_user.return_value = False

        result = self.login_module.login(uid='nonexistent_user', token='test_token')

        self.assertIsNone(result)
        self.assertEqual(self.mock_password_module.get_user.call_count, 0)

    def test_login_user_invalid_password(self):
        # Mock data from the secure storage
        mock_data = {
            'username': 'test_user',
            'role': 'C',
            'password': 'StrongP@ssword1',
            'attributes': {'test': 'test'}
        }

        # Set the return value for the retrieve_secret method
        self.mock_secure_storage.retrieve_secret.return_value = 'Invalid_Password'

        # Set the return value for the is_user method (user exists)
        self.mock_password_module.is_user.return_value = True

        # Set the return value for the get_user method. wrong password returns None
        self.mock_password_module.get_user.return_value = None

        result = self.login_module.login(uid='test_user', token='test_token')

        # Assert that the login failed due to an invalid password
        self.assertIsNone(result)

        #assert that get_user is called 
        self.assertEqual(self.mock_password_module.get_user.call_count, 1)

if __name__ == '__main__':
    unittest.main()
