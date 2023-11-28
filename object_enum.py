from enum import Enum

class Objects(Enum):
    View_Balance = 'VB'
    View_Investment_Portfolio = 'VIP'
    Modify_Investment_Portfolio = 'MIP'
    Get_Contact_of_Financial_Advisor = 'GCOFA'
    Get_Contact_of_Financial_Planner = 'GCOFP'
    Get_Contact_of_Investment_Analyst = 'GCOIA'
    View_Money_Market_Instruments = 'VMMI'
    View_Private_Consumer_Instruments = 'VPCI'
    View_Interest_Instrumnets = 'VII'
    View_Derivatives_Trading = 'VDT'
    Validate_Investment_Portfolio_Modifications = 'VIPM'
    View_Client_Info = 'VCI'
    Request_Client_Account_Access = 'RCAA'