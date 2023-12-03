from password_module import PasswordModule
from subject_enum import Subjects
from secure_storage import SecureStorage
import re
class EnrollmentModule:

    def __init__(self, secure_storage: SecureStorage, password_module) -> None:
        self._password_module = password_module
        self._storage = secure_storage

    def enroll_user(self, token):

        user_info = self._storage.retrieve_secret("new_user", token)

        username = user_info['username']
        role = user_info['role']
        password = user_info['password']
        attributes = user_info["attributes"]

        if not self._is_unique_username(username):
            print("Username " + username + " is unavailable")
            return False
        
        if username == password:
            print("Username and password cannot match")
            return False
        
        if ":" in username:
            print("Invalid character in username")
            return False
        
        if not self._is_valid_password(password):
            print("This password is not strong enough. Please ensure your password meets all these requirement")
            print("- Atleast 8 characters long")
            print("- Contains atleast 1 uppercase letter")
            print("- Contains atleast 1 lowercase letter")
            print("- Contains atleast 1 symbol")
            print("- Not in the format of a license plate, phone number, or date")
            return False
        
        if not Subjects.is_valid_enum_value(role):
            print("Please select a valid role")
            return False
        
        self._password_module.add_pass(username=username, role=role, password=password, attributes=attributes)
        return True

    def _is_unique_username(self, username):
        return not self._password_module.is_user(username)
    

    def _is_valid_password(self, password):    
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
        
        if not self._proactive_pass_check(password):
            return False

        return True
    
    def _proactive_pass_check(self, password):
        with open('common_passwords.txt', 'r') as file:
            for common_pass in file:
                if common_pass == password:
                    return False
        
        return True