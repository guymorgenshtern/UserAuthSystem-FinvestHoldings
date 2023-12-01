from access_control_matrix import AccessControlMatrix
from policy_rules_store import PolicyRulesStore, Policy
from object_enum import Objects
from subject_enum import Subjects
from datetime import datetime, time

class AccessControlSystem:
    
    def __init__(self) -> None:
        self.control_matrix = AccessControlMatrix()
        self.policy_store = PolicyRulesStore()

        def outside_business_hours():
            current_time = datetime.now().time()

            # Define the time range (10 am to 4 pm)
            start_time = time(10, 0)
            end_time = time(16, 0)
            return not (current_time >= start_time and current_time <= end_time)
        
        revoke_teller_balance_access_past_business_hours = Policy(Objects.View_Balance.value,{"role": Subjects.Teller.value}, environmental_condition=outside_business_hours)
        revoke_teller_portfolio_access_past_business_hours = Policy(Objects.View_Investment_Portfolio.value,{"role": Subjects.Teller.value}, environmental_condition=outside_business_hours)
        self.policy_store.add_policy(revoke_teller_balance_access_past_business_hours)
        self.policy_store.add_policy(revoke_teller_portfolio_access_past_business_hours)


    def check_authorization(self, subject, object) -> bool:
        # in this system, the access control matrix is responsible for determining who has access to the system
        # the policy store handles special conditions (i.e Tellers can't access system past business hours)
        # if the policy store evaluates TRUE on a subject-object pair, then access is DENIED, otherwise the matrix is consulted

        if self.policy_store.evaluate_all_policies(object, subject):
            return False
        else:
            return self.control_matrix.check_permission(subject['role'], object)
    


x = AccessControlSystem()

first_dimension_keys = list(x.control_matrix.permissions_by_object_subject_matrix.keys())
second_dimension_keys = list(x.control_matrix.permissions_by_object_subject_matrix[first_dimension_keys[0]].keys())

p = ""
for obj in second_dimension_keys:
    p += obj + ","
print(p)

for first_key in first_dimension_keys:
    s = first_key + ","
    for second_key in second_dimension_keys:
        if x.check_authorization({'role': first_key}, second_key):
             s += "X"
        else:
            s += "-"
        s+= ","
    print(s)
    
        

print(x.control_matrix.permissions_by_object_subject_matrix[Subjects.Technical_Support.value][Objects.View_Client_Info.value])


# VB,VIP,MIP,GCOFA,GCOFP,GCOIA,VMMI,VPCI,VII,VDT,VIPM,VCI,RCAA,
# C,X,X,,X,,,,,,,,,
# PC,X,X,X,X,X,X,,,,,,,
# E,X,X,,,,,,,,,,,
# FP,X,X,X,,,,X,X,,,,,
# FA,X,X,X,,,,,X,,,,,
# IA,X,X,X,,,,X,X,X,X,,,
# TS,,,,,,,,,,,,,X
# T,,,,,,,,,,,,,
# CO,X,X,,,,,,,,,X,,

    