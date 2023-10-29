import pandas as pd
import os
from dateutil.parser import parse


def load_data(file_path):
    pwd = os.getcwd()
    df = pd.read_csv(pwd + file_path)
    print(df.info())
    return df


df = load_data("/dataset/loan_data.csv")
print(df.dtypes)

# print(dt)

# Are there columns that could be represented better numerically, are dates in the correct format, should some columns be categorical? Are there any excess symbols in the data?

# Unnamed data remove
# loan_amount, never need decimal place?
# funded amount, decimal place?
# term - obj -> date
# installment
# loan grade -> string
# employment length - object -> months?
# ownership -> type -> string
# issue date -> obj -> date
# loan_status -> NEEDS MORE LOOKS
# payment_plan -> boolean
# delinq_2yrs fine int for month
# earliest credit_line object to date
# 'mths_since_last_delinq' -> INT and trim
#  last_payment_date
# ext_payment_date
# last_credit_pull_date
# application_type need?
# grade, subgrade, purpose = categorical
