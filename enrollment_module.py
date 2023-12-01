from password_module import PasswordModule
from subject_enum import Subjects
import re
class EnrollmentModule:

    def __init__(self) -> None:
        self._password_module = PasswordModule()

    def enroll_user(self, username, role, password):

        if not self._is_unique_username(self, username):
            print("Username " + username + " is unavailable")
            return False
        
        if username == password:
            print("Username and password cannot match")
            return False
        
        if not self._is_valid_password(self, password):
            print("This password is not strong enough. Please ensure your password meets all these requirement")
            print("- Atleast 8 characters long")
            print("- Contains atleast 1 uppercase letter")
            print("- Contains atleast 1 lowercase letter")
            print("- Contains atleast 1 symbol")
            print("- Not in the format of a license plate, phone number, or date")
            return False
        
        if not role in Subjects._member_map_:
            print("Please select a valid role")
            return False
        
        self._password_module.add_pass(username=username, role=role, password=password)

    def _is_unique_username(self, username):
        with open('password_file.txt', 'r') as file:
            for line in file:
                values = line.strip().split(":")
                if values[0] == username:
                    return False
        
        return True
    

    def _is_valid_password(password):    
        # Check length
        if not 8 <= len(password):
            return False

        # Check for at least one upper-case letter
        if not re.search(r'[A-Z]', password):
            return False

        # Check for at least one lower-case letter
        if not re.search(r'[a-z]', password):
            return False

        # Check for at least one numerical digit
        if not re.search(r'\d', password):
            return False

        # Check for at least one special character
        if not re.search(r'[!@#$%?\*]', password):
            return False

        # Check for prohibited formats (calendar dates, license plate numbers, telephone numbers)
        if re.search(r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b', password) or \
        re.search(r'\b\d{1,3}[A-Za-z]\d{1,4}\b', password) or \
        re.search(r'\b\d{3}[./-]\d{3}[./-]\d{4}\b', password):
            return False

        return True
    
    def _proactive_pass_check(self, password):
        with open('common_passwords.txt', 'r') as file:
            for common_pass in file:
                if common_pass == password:
                    return False
        
        return True
    

import secrets

class PasswordManager:
    def __init__(self):
        self._temporary_storage = {}

    def store_password(self, user_id, password):
        # Use secrets.token_hex to generate a secure token
        secure_token = secrets.token_hex(16)
        self._temporary_storage[user_id] = (password, secure_token)

    def retrieve_password(self, user_id, entered_token):
        # Check if the user_id exists in the temporary storage
        if user_id in self._temporary_storage:
            stored_password, secure_token = self._temporary_storage[user_id]

            # Check if the entered token matches the stored secure token
            if secure_token == entered_token:
                return stored_password

        return None

# Example usage
password_manager = PasswordManager()

# Storing a password securely
user_id = "user123"
password_to_store = "my_secure_password"
password_manager.store_password(user_id, password_to_store)

# Retrieving the password securely (simulating a user entering a secure token)
entered_secure_token = password_manager._temporary_storage[user_id][1]
retrieved_password = password_manager.retrieve_password(user_id, entered_secure_token)

print(f"Retrieved Password: {retrieved_password}")
