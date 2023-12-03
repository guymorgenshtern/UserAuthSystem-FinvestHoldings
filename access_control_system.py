from access_control_matrix import AccessControlMatrix
from policy_rules_store import PolicyRulesStore, Policy

class AccessControlSystem:
    
    def __init__(self) -> None:
        self.control_matrix = AccessControlMatrix()
        self.policy_store = PolicyRulesStore()


    def check_authorization(self, subject, object) -> bool:
        # in this system, the access control matrix is responsible for determining who has access to the system
        # the policy store handles special conditions (i.e Tellers can't access system past business hours)
        # if the policy store evaluates TRUE on a subject-object pair, then access is DENIED, otherwise the matrix is consulted
   
        if self.policy_store.evaluate_all_policies(object, subject.attributes):
            return False
        else:
            return self.control_matrix.check_permission(subject.role, object)
    
    