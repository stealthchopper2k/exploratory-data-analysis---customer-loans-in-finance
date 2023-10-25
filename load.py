import pandas as pd
import os


def load_data(file_path):
    pwd = os.getcwd()
    df = pd.read_csv(pwd + file_path)
    print(df.info())
    return df


load_data("/dataset/loan_data.csv")
