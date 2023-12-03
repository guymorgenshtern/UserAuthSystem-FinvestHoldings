from enum import Enum

class Subjects(Enum):
    Client = 'C'
    Premium_Client = 'PC'
    Employee = 'E'
    Financial_Planner = 'FP'
    Financial_Advisor = 'FA'
    Investment_Analyst = 'IA'
    Technical_Support = 'TS'
    Teller = 'T'
    Compliance_Officer = 'CO'

    def is_valid_enum_value(input_str):

        # Check if the input_str is a value in the Objects enum
        return any(input_str == sbj.value for sbj in Subjects)
    
    def to_string():

        s = ""
        for sbj in Subjects:
            s +=(f"{sbj.name} ({sbj.value}) \n")

        return s