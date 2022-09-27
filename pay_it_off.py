import pyinputplus as pyip
import numpy as np
import numpy_financial as npf
'''A program to calculate how long it would take to pay off something such as a car loan.'''
'''Steps
1) Get input: a)done  b)done
c) all except hourly (not sure if needed)
d) Mandatory Bills / optionally additional expenses

2) Calculate how long it would take to pay off based on income/expenses

3) Return: Message showing time to pay off given parameters, and total payed off(including interest)'''


def get_loan_info():
    print('Hello, and welcome to the Pay It Off program!')
    print('Just enter the requested information, and it calculates')
    print('how long it would take to pay a given debt off.\n')
    print("Let us begin!\n")
    
    debt_amount = pyip.inputNum("How much is the loan you'd like to pay off?\n", greaterThan=0)
    verify_debt = pyip.inputYesNo(
        f'You want to know how long it would take to pay off ${debt_amount:,.2f}, is this correct?(y,n)\n')
    
    while verify_debt == 'no':
        debt_amount = pyip.inputNum(
            "How much is the loan you'd like to pay off?\n", greaterThan=0)
        verify_debt = pyip.inputYesNo(
        f'You want to know how long it would take to pay off ${debt_amount:,.2f}, is this correct?(y/n)\n')
    
    include_interest = pyip.inputYesNo(
        'Would you like to calculate for interest?(y,n)\n')
    
    if include_interest == 'yes':
        interest_rate = pyip.inputNum('What is the annual interest rate of this loan?\n', greaterThan=0)
        verify_interest = pyip.inputYesNo(
            f'The loan has an annual interest rate of {interest_rate}%, is this correct?(y/n)\n')
        while verify_interest == 'no':
            interest_rate = pyip.inputNum(
                'What is the annual interest rate of this loan?\n', greaterThan=0)
            verify_interest = pyip.inputYesNo(
                f'The loan has an annual interest rate of {interest_rate}%, is this correct?(y/n)\n')
            
    print(f'Loan Debt: ${debt_amount}')
    if include_interest == "yes":
        print(f'Annual Interest Rate: {interest_rate}%')
        return debt_amount, interest_rate
    return debt_amount

def get_income_info():
    
    print("\nNow let's get some income information!\n")
    
    paycheck = pyip.inputNum('How much is your paycheck after taxes/deductions?\n', greaterThan=0)
    verify_check = pyip.inputYesNo(
        f'You make ${paycheck:,.2f} per paycheck, is this correct?(y/n)\n')
    while verify_check == 'no':
        paycheck = pyip.inputNum(
            'How much is your paycheck after taxes/deductions?\n', greaterThan=0)
        verify_check = pyip.inputYesNo(
            f'You make ${paycheck:,.2f} per paycheck, is this correct?(y/n)\n')
    
    pay_schedule = pyip.inputMenu(
        ['Daily', 'Weekly', 'Biweekly', 'Monthly'], 'How often are you paid?\n', numbered=True)
    verify_pay_schedule = pyip.inputYesNo(
        f'You are paid {pay_schedule.lower()}, is this correct?(y/n)\n')
    while verify_pay_schedule == 'no':
        pay_schedule = pyip.inputMenu(
            ['Daily', 'Weekly', 'Biweekly', 'Monthly'], 'How often are you paid?\n', numbered=True)
        verify_pay_schedule = pyip.inputYesNo(
            f'You are paid {pay_schedule.lower()}, is this correct?(y/n)\n')
    
    print(f'Net Income: ${paycheck:,.2f} {pay_schedule.lower()}')

def number_crunch():
    debt_info = get_loan_info()
    
    # Assigning return values of debt info to variables to use in calcs.
    if len(debt_info) > 1: # If get_loan_info returns more than 1 val, interest was included.
        debt_principal = debt_info[0] # Unpack to vars.
        annual_interest = debt_info[1] / 100
        print(f'NC Debt_princ: {debt_principal} NC Ann-interest {annual_interest}\n')
    else:
        debt_principal = debt_info[0]
        print(f'NC Debt_princ: {debt_principal}') # Else just debt
          
    # This calcs months to pay off based on payment per month
    months_to_pay = np.round(npf.nper(annual_interest/12, -200, debt_principal))
    # collect payment_cash which will be what user can spare, (income - mandatory bills = max_extra_cash)
    print(f'It will take ~{int(months_to_pay)} months to pay off your loan with monthly payments of 200$.')
    print(f'This equates to ~{int(months_to_pay)/12:.2f} years.')
        
    
    income = get_income_info()
    
    
    
    
def ideal_world():
    pass
def real_world():
    pass
def main():
    number_crunch()
    print('Done')
  
    
main()
