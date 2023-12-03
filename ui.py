from subject_enum import Subjects
from object_enum import Objects
from enrollment_module import EnrollmentModule
from login_module import LoginModule
from secure_storage import SecureStorage
from access_control_system import AccessControlSystem

class System:

    def __init__(self) -> None:
        self.storage = SecureStorage()
        self.enrollment = EnrollmentModule(self.storage)
        self.login = LoginModule(self.storage)
        self.access_control_system = AccessControlSystem()
        self.user = None
    
    def access_resource(self, resource):
        while resource != 'quit':
            if Objects.is_valid_enum_value(resource):
                
                return self.access_control_system.check_authorization(self.user, resource)

            else: 
                print("Select a valid resource or 'quit' to logout ")
                return False
        
    
    def print_current_permissions(self):

        print(f"-------------Permissions {self.user.username}: {self.user.role}: {self.user.attributes}-------------")
        for r in Objects:
            print(f"{r.name} - {r.value}: {self.access_control_system.check_authorization(self.user, r.value)}")
            


    def login_or_enrollment(self):

        while self.user is None:
            action = input("1. Enroll user\n2. Login\nChoose an option (1 or 2): ")   
            if action == '1':

                enrolled = False
                while not enrolled:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    role_input = input("Enter role \n" + Subjects.to_string())

                    print("Enter attributes (optional): ")
                    attributes = {}
                    while True:
                        key = input("Enter a name for the attribute: (press Enter to stop): ")

                        # If the user presses Enter without entering a key, break out of the loop
                        if not key:
                            break

                        value = input("Enter a value for that attribute (press Enter to skip): ")

                        # If the user provides both key and value, add them to the dictionary
                        if key and value:
                            attributes[key] = value


                    token = self.storage.store_secret("new_user", {"username": username, "password": password, "role": role_input, "attributes": attributes})
                    enrolled = self.enrollment.enroll_user(token)
                
                print("Successfully enrolled!")



            elif action == '2':

                while self.user is None:
                    username = input("Enter username: ")
                    password = input("Enter password: ")

                    token = self.storage.store_secret(username, password)
                    self.user = self.login.login(username, token)
                
                print(f"Logged in as: {self.user.username} - {self.user.role} - {self.user.attributes}")
    


    def boot(self):
        self.login_or_enrollment()

        if self.user is not None:
            self.print_current_permissions()
            resource = input("What would you like to access \n")
            while resource != 'quit':

                access = self.access_resource(resource)
                print("-----------------------------")
                print(f"User: {self.user.username} Role: {self.user.role} Attributes: {self.user.attributes}")
                if access:
                    print(f"Access to {resource}: GRANTED ")

                else: 
                    print(f"Access to {resource}: DENIED ")

                print("-----------------------------")       
                
                resource = input("What would you like to access (enter 'quit' to logout) \n" + Objects.to_string())
            
x = System()



x.boot()