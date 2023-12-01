import bcrypt

class PasswordModule:
   
    def __init__(self) -> None:
        pass


    def add_pass(self, username, role, password):
        record_data = self._make_password_record(username, role, password)

        with open('password_file.txt', 'a') as file:
            file.write(str(record_data['username']) + ":" + record_data['role'] + ":" + record_data['salt'] + ":" + record_data['hashed_password'] + "\n")


    def _make_password_record(self, username, role, password, salt_runs: int = 12):        
        salt = bcrypt.gensalt(salt_runs)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        str_hashed_pass = hashed_password.decode('utf-8')

        password_data = {
            'username': username,
            'role': role,
            'salt': salt.decode('utf-8'),  
            'hashed_password': str_hashed_pass, 
        }
        return password_data
    
    def check_pass(self, username, password) -> bool:
        with open('password_file.txt', 'r') as file:
            # Iterate through each line
            for line in file:
                # Process each line
                values = line.strip().split(":")
                if values[0] == username:
                    encoded_user_input = password.encode('utf-8')
                    encoded_salt = values[2].encode('utf-8')
                    encoded_pass = values[3].encode('utf-8')
        
                    hashed_user_input = bcrypt.hashpw(encoded_user_input,encoded_salt)
                    print (hashed_user_input)
                    print (encoded_pass)
                    print (hashed_user_input == encoded_pass)
                    if hashed_user_input == encoded_pass:
                        return True
        
        return False
