import unittest
from password_module import PasswordModule
import os
class TestPasswordModule(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file_path = "test_passwd.txt"
        self.temp_file = open(self.temp_file_path, "w+")


        # Initialize the PasswordModule with the temporary file
        self.password_module = PasswordModule(file_name=self.temp_file_path)

    def tearDown(self):
        # Clean up the temporary file
        self.temp_file.close()
        os.remove("test_passwd.txt")

    def test_add_and_check_password(self):
        username = "test_user"
        role = "admin"
        password = "test_password"
        attributes = {"email": "test@example.com"}

        # Add a password
        self.password_module.add_pass(username, role, password, attributes)

        # Check the password
        result = self.password_module.check_pass(username, password)
        self.assertTrue(result)

    def test_nonexistent_user(self):
        username = "nonexistent_user"
        password = "some_password"

        # Check a password for a user that doesn't exist
        result = self.password_module.check_pass(username, password)
        self.assertFalse(result)

    def test_is_user(self):
        username = "existing_user"

        # Add a user
        self.password_module.add_pass(username, "user_role", "user_password", {})

        # Check if the user exists
        result = self.password_module.is_user(username)
        self.assertTrue(result)

    def test_nonexistent_is_user(self):
        username = "nonexistent_user"

        # Check if a nonexistent user exists
        result = self.password_module.is_user(username)
        self.assertFalse(result)

    def test_get_user(self):
        username = "test_user"
        role = "C"
        password = "test_password"
        attributes = {"test": "test"}

        # Add a user
        self.password_module.add_pass(username, role, password, attributes)

        # Get the user
        user = self.password_module.get_user(username, password)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, username)
        self.assertEqual(user.role, role)

        attributes.update({'role': role})
        self.assertEqual(user.attributes, attributes)

    def test_nonexistent_get_user(self):
        username = "nonexistent_user"
        password = "some_password"

        # Get a nonexistent user
        user = self.password_module.get_user(username, password)
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()