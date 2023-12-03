import bcrypt
from user import User

class PasswordModule:

    _passwd_file = "passwd.txt"

    def add_pass(self, username, role, password, attributes):
        record_data = self._make_password_record(username=username, role=role, password=password, attributes=attributes)

        with open(self._passwd_file, 'a') as file:
            str_attributes = str(record_data['attributes']).replace(":", ";")
            file.write(str(record_data['username']) + ":" + record_data['role'] + ":" 
                       + str_attributes + ":" + record_data['salt'] + ":" + record_data['hashed_password'] + "\n")


    def _make_password_record(self, username, role, password, attributes, salt_runs: int = 12):        
        salt = bcrypt.gensalt(salt_runs)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        str_hashed_pass = hashed_password.decode('utf-8')

        password_data = {
            'username': username,
            'role': role,
            'attributes': attributes if attributes is not None else {},
            'salt': salt.decode('utf-8'),  
            'hashed_password': str_hashed_pass, 
        }
        return password_data
    
    def check_pass(self, username, password):
        with open(self._passwd_file, 'r') as file:
            # Iterate through each line
            for line in file:
                # Process each line
                values = line.strip().split(":")
                if values[0] == username:
                    encoded_user_input = password.encode('utf-8')
                    encoded_salt = values[3].encode('utf-8')
                    encoded_pass = values[4].encode('utf-8')
        
                    hashed_user_input = bcrypt.hashpw(encoded_user_input,encoded_salt)

                    if hashed_user_input == encoded_pass:
                        return True
        
        return False
    
    def is_user(self, username):
         with open(self._passwd_file, 'r') as file:
            # Iterate through each line
                for line in file:
                # Process each line
                    values = line.strip().split(":")
                    if values[0] == username:
                        return True
    

    def get_user(self, username, password):
        if self.check_pass(username, password):
            with open(self._passwd_file, 'r') as file:
            # Iterate through each line
                for line in file:
                # Process each line
                    values = line.strip().split(":")
                    if values[0] == username:
                        return User(values[0], values[1], eval(values[2].replace(";", ":")))
        
        return None
    
