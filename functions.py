from Loan import *
import pandas as pd
from datetime import date
column_name = ['Month', 'Begin Principal', 'Payment', 'Extra Payment',
                         'Applied Principal', 'Applied Interest', 'End Principal']

def disting(a):
    if a == None:
        b = 0
    else:
        b = a
    return b

def date_trans(df,start_date):
    m = start_date.month
    y = start_date.year
    list_1=[]
    for i in list(df['Month']):
        new_m = (m + int(i) - 1) % 12 + 1
        new_y = y + (m + int(i) - 1) //12
        new_date = date(new_y, new_m, start_date.day)
        list_1.append(new_date)
    df['Month'] = list_1
    return df

def to_df(loan):
    loan.check_loan_parameters()
    loan.compute_schedule()
    df = pd.DataFrame(columns = ['Month', 'Begin Principal', 'Payment', 'Extra Payment','Applied Principal', 'Applied Interest', 'End Principal'])
    for pay in loan.schedule.values():
        df = df.append({'Month':round(pay[0],2),'Begin Principal':round(pay[1],2),'Payment':round(pay[2],2),'Extra Payment':round(pay[3],2),'Applied Principal':round(pay[4],2),'Applied Interest':round(pay[5],2),'End Principal':round(pay[6],2)},ignore_index = True)
    return df 

def compute_schedule_loan(principal, rate, payment, extra_payment):
    loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
    loan.check_loan_parameters()
    loan.compute_schedule()
    return round(loan.total_principal_paid, 2) + round(loan.total_interest_paid, 2), round(loan.total_interest_paid, 2), round(loan.time_to_loan_termination, 0)
    
