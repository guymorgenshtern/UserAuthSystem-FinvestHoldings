from secure_storage import SecureStorage
from password_module import PasswordModule
from enrollment_module import EnrollmentModule
class LoginModule:

    def __init__(self, storage: SecureStorage, password_module: PasswordModule) -> None:
        self._storage = storage
        self._password_module = password_module
    
    def login(self, uid, token):
        
        if self._password_module.is_user(uid):
            password = self._storage.retrieve_secret(uid, token)

            user = self._password_module.get_user(uid, password)
            if user is not None:
                return user
            else:
                print("Your username or password do not match")
        
        else: print("User " + uid + " does not exist")

            




