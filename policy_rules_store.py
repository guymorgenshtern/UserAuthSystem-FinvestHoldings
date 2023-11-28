from datetime import datetime, time
class Policy:
    def __init__(self, resource, attributes, environmental_condition: callable = None) -> None:
        self.resource = resource
        self.attributes = attributes
        self.environmental_condition = environmental_condition
    

    def evaluate(self, resource, attributes_of_user):

        if resource == self.resource:
            for user_attribute in attributes_of_user.keys():
                if user_attribute in self.attributes and attributes_of_user[user_attribute] == self.attributes[user_attribute]:
                    if self.environmental_condition != None:
                        return self.environmental_condition()
                    else:
                        return True
                
        return False
    

class PolicyRulesStore:

    def __init__(self) -> None:
        self.policies = []

    def add_policy(self, policy: Policy):
        self.policies.append(policy)
    
    def evaluate_all_policies(self, resource, attributes_of_user: dict): 
        for policy in self.policies:
            if policy.evaluate(resource, attributes_of_user):
                return True
        
        return False
    


# store = PolicyRulesStore()

# def date_check():
#     current_time = datetime.now().time()

#     # Define the time range (10 am to 4 pm)
#     start_time = time(10, 0)
#     end_time = time(21, 0)
#     return current_time >= start_time and current_time <= end_time
# p1 = Policy("account",{"user": "guy"}, environmental_condition=date_check)
# p2 = Policy("account",{"user": "greg"}, environmental_condition=date_check)
# p3 = Policy("r",{"user": "guy"}, environmental_condition=date_check)

# store.add_policy(p1)
# store.add_policy(p2)
# store.add_policy(p3)

# print(store.evaluate_all_policies("account",{"user": "guy"}))