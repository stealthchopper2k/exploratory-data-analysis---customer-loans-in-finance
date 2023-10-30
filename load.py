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
print(df.info())
