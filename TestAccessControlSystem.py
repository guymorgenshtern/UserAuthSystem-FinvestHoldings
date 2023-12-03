import unittest
from datetime import datetime, time
from access_control_system import AccessControlSystem  
from subject_enum import Subjects
from object_enum import Objects
from user import User
from policy_rules_store import Policy
class TestSystem(unittest.TestCase):

    def test_check_authorization_during_business_hours(self):
        # Create an instance of AccessControlSystem
        access_control_system = AccessControlSystem()

        def outside_business_hours():
            return False
        
        revoke_teller_balance_access_past_business_hours = Policy(Objects.View_Balance.value,{"role": Subjects.Teller.value}, environmental_condition=outside_business_hours)
        revoke_teller_portfolio_access_past_business_hours = Policy(Objects.View_Investment_Portfolio.value,{"role": Subjects.Teller.value}, environmental_condition=outside_business_hours)
        access_control_system.policy_store.add_policy(revoke_teller_balance_access_past_business_hours)
        access_control_system.policy_store.add_policy(revoke_teller_portfolio_access_past_business_hours)


        subject = User(username="test", role=Subjects.Teller.value, attributes={})
        object = Objects.View_Balance.value

        # Ensure check_authorization returns True (access is allowed)
        result = access_control_system.check_authorization(subject, object)
        self.assertTrue(result)

    def test_check_authorization_outside_business_hours(self):
        access_control_system = AccessControlSystem()


        def outside_business_hours():
            return True
        
        revoke_teller_balance_access_past_business_hours = Policy(Objects.View_Balance.value,{"role": Subjects.Teller.value}, environmental_condition=outside_business_hours)
        revoke_teller_portfolio_access_past_business_hours = Policy(Objects.View_Investment_Portfolio.value,{"role": Subjects.Teller.value}, environmental_condition=outside_business_hours)
        access_control_system.policy_store.add_policy(revoke_teller_balance_access_past_business_hours)
        access_control_system.policy_store.add_policy(revoke_teller_portfolio_access_past_business_hours)

        subject = User(username="test", role=Subjects.Teller.value, attributes={})
        object = Objects.View_Balance.value

        # Mock current time outside business hours (7 pm)
        result = access_control_system.check_authorization(subject, object)
        self.assertFalse(result)

    def test_permission_denied(self):
        access_control_system = AccessControlSystem()

        subject = User(username="test", role=Subjects.Client.value, attributes={})
        object = Objects.View_Money_Market_Instruments.value

        # Mock current time outside business hours (7 pm)
        result = access_control_system.check_authorization(subject, object)
        self.assertFalse(result)


        
if __name__ == '__main__':
    unittest.main()
