import pyinputplus as pyip
import numpy as np
import numpy_financial as npf
import datetime
from dateutil import relativedelta

def get_loan_info():
    print('\nHello, and welcome to the Pay It Off program!')
    print('\nJust enter the requested information, and it calculates')
    print('how long it would take to pay a given debt off.\n')
    print("Let us begin!\n")
    
    debt_amount = pyip.inputNum("How much is the loan you'd like to pay off?\n", greaterThan=0)
    verify_debt = pyip.inputYesNo(
        f'You want to know how long it would take to pay off ${debt_amount:,.2f}, is this correct?(y/n)\n')
    
    while verify_debt == 'no':
        debt_amount = pyip.inputNum(
            "How much is the loan you'd like to pay off?\n", greaterThan=0)
        verify_debt = pyip.inputYesNo(
        f'You want to know how long it would take to pay off ${debt_amount:,.2f}, is this correct?(y/n)\n')
    
    loan_term = pyip.inputInt('How many years do you have to pay the loan?\n', greaterThan=0)
    verify_term = pyip.inputYesNo(f'It is a {loan_term} year loan, correct?(y/n)')
    while verify_term =='no':
        loan_term = pyip.inputInt(
            'How many years do you have to pay the loan?\n', greaterThan=0)
        verify_term = pyip.inputYesNo(
            f'It is a {loan_term} year loan, correct?(y/n)')
        
    # 2026-05-26
    deadline_date = pyip.inputDate("What is the date of the loan repayment deadline?(YYYY/MM/DD)\n")
    verify_deadline = pyip.inputYesNo(
        f'You must pay the loan off by {deadline_date}, is this correct?(y/n)\n')
    
    while verify_deadline == 'no':
        deadline_date = pyip.inputDate(
            "What is the date of the loan repayment deadline?(YYYY/MM/DD)\n")
        verify_deadline = pyip.inputYesNo(
            f'You must pay the loan off by {deadline_date}, is this correct?(y/n)\n')
        
    include_interest = pyip.inputYesNo(
        'Would you like to calculate for interest?(y/n)\n')
    
    if include_interest == 'yes':
        interest_rate = pyip.inputNum('What is the annual interest rate of this loan?\n', greaterThan=0)
        verify_interest = pyip.inputYesNo(
            f'The loan has an annual interest rate of {interest_rate}%, is this correct?(y/n)\n')
        while verify_interest == 'no':
            interest_rate = pyip.inputNum(
                'What is the annual interest rate of this loan?\n', greaterThan=0)
            verify_interest = pyip.inputYesNo(
                f'The loan has an annual interest rate of {interest_rate}%, is this correct?(y/n)\n')
            
    print(f'Loan Debt: ${debt_amount:,.2f}')
    print(f'Repayment Deadline: {deadline_date}')
    print(f'Loan Term: {loan_term}')
    if include_interest == "yes":
        print(f'Annual Interest Rate: {interest_rate}%')
        return debt_amount, interest_rate, deadline_date, loan_term
    return debt_amount, deadline_date, loan_term

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
    
    # Convert all pay schedules to monthly for easier math later.
    match pay_schedule:
        case 'Daily':
            mo_income = (30.4 * paycheck)  # Avg days in month
        case 'Weekly':
            mo_income = (4 * paycheck)
        case 'Biweekly':
            mo_income = (2 * paycheck)
        case 'Monthly':
            mo_income = paycheck
   
    return mo_income

def get_expense_info():
    
    print('\nNow to account for expenses.\n')
    expenses = {}
    while True:
        expense_name = pyip.inputMenu(['Rent', 'Food', 'Gas', 'Phone', 'Insurance', 'Optional'],
                                      "Please choose each bill you pay and then enter a value.\n", numbered=True)
        if expense_name == 'Optional':
            expense_name = pyip.inputStr('Which optional bill is this?\n')
        expense_val = pyip.inputNum("How much is this bill?\n", greaterThan=0)
        expenses[expense_name] = expense_val
        another_yn = pyip.inputYesNo("Enter another expense?(y/n)\n")
        if another_yn == 'no':
            break
    print('\nExpenses:\n')
    print('-'*40)
    for k, val in expenses.items():
        print(f'{k:<25} ${val:>10,.2f}')
    
    total_expenses = sum(expenses.values())
    print(f'{"Total Monthly Spending":<25} ${total_expenses:>10,.2f}')
    
    return total_expenses
      
def number_crunch():
    # This assigns return values of get loan info function to a tuple called debt_info
    debt_info = get_loan_info()
    
    # Assigning return values (principal, interest) to variables to use in calcs.
    if len(debt_info) > 3: # If get_loan_info returns more than 1 val, interest was included.
        debt_principal = debt_info[0] # Unpack to variables.
        annual_interest = debt_info[1] / 100
        deadline_date = debt_info[2]
        loan_term = debt_info[3]
    else:
        debt_principal = debt_info[0]
        annual_interest = 0
        deadline_date = debt_info[1]
        loan_term = debt_info[2]
        
    # Get monthly income
    income_info = get_income_info() # Returns monthly income
    
    # Gets total monthly expenses
    expense_info = get_expense_info()
    
    # Get today's date
    today = datetime.date.today()
    # Calculate difference between today and repayment deadline.
    difference = relativedelta.relativedelta(deadline_date, today)
    # Convert this to remaining months.
    months_left = (difference.years * 12) + difference.months
    loan_term_mo = loan_term * 12
    
    # Given the mandatory+optional spending in expenses, calculate left over cash
    max_extra_cash = income_info - expense_info
    print(f'\nBased on a monthly net income of ${income_info:,.2f} and total monthly expenses of ${expense_info:,.2f}, \nyou have ~${max_extra_cash:,.2f} left as surplus cash per month.')
    if loan_term_mo > difference: # If the difference from today to deadline is within loan terms, use that diff as var.
        if annual_interest == 0: # If no interest
            min_payment = npf.pmt(annual_interest/12, 
                                months_left, debt_principal)*-1
            max_months_to_pay = np.round(
                npf.nper(annual_interest/12, min_payment, debt_principal), 1)
            min_months_to_pay = np.round(
                npf.nper(annual_interest/12, max_extra_cash, debt_principal), 1)
        else:
            # This calcs minimum payment based on months til deadline/interest/and amount borrowed
            min_payment = npf.pmt(
                annual_interest/12, months_left, debt_principal)*-1
            # This uses minimum payments, returns longest time to pay off remaining debt within deadline
            max_months_to_pay = np.round(
                npf.nper(annual_interest/12, -min_payment, debt_principal), 1)
            # This uses surplus cash, if all spent on paying off, returns min months to payoff
            min_months_to_pay = np.round(
                npf.nper(annual_interest/12, -max_extra_cash, debt_principal), 1)
    else: # If time til deadline is over the loan term, means the loan hasn't started. 
        if annual_interest == 0:
            min_payment = npf.pmt(annual_interest/12,
                                  loan_term_mo, debt_principal)*-1
            max_months_to_pay = np.round(
                npf.nper(annual_interest/12, min_payment, debt_principal), 1)
            min_months_to_pay = np.round(
                npf.nper(annual_interest/12, max_extra_cash, debt_principal), 1)
        else:
            min_payment = npf.pmt(
                annual_interest/12, loan_term_mo, debt_principal)*-1
            max_months_to_pay = np.round(
                npf.nper(annual_interest/12, -min_payment, debt_principal), 1)
            min_months_to_pay = np.round(
                npf.nper(annual_interest/12, -max_extra_cash, debt_principal), 1)
    # Calculate total paid, and savings.
    max_grand_total = min_payment * max_months_to_pay
    min_grand_total = max_extra_cash * min_months_to_pay
    savings = max_grand_total - min_grand_total
    
    print(
        f'\nUsing the minimum payment of ${min_payment:,.2f}, you have ~{int(max_months_to_pay)} more months until the loan is repayed.')
    print(
        f'This equates to ~{int(max_months_to_pay)/12:.2f} years and a grand total paid of ~${(max_grand_total):,.2f}\n')
    
    print(
        f'If you instead put all your surplus income (${max_extra_cash:,.2f}) towards paying off the loan each month, \nit would only take ~{min_months_to_pay} months to pay it off!')
    print(
        f'You would pay a grand total of ~${(min_grand_total):,.2f}, saving yourself roughly ${savings:,.2f}!')
    
    
    pass

def main():
    number_crunch()
  
main()

'''To do:
Use PyGui/ another module to create a GUI using this program for logic.
Replicate project using classes.
Create a pretty website using HTML/CSS/JS and port this over.
Create a site using flask/django and port this over.'''
