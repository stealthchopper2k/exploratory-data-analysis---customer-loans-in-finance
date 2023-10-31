from numpy import save
import yaml
from sqlalchemy import create_engine
import pandas as pd
import os
from pathlib import Path


def load_credentials():
    with open('./credentials.yaml', 'r') as f:
        try:
            content = yaml.safe_load(f)
            return content
        except yaml.YAMLError as e:
            print(e)


def load_data(file_path):
    pwd = os.getcwd()
    df = pd.read_csv(pwd + file_path)
    return df


class RDSDatabaseConnector:
    def __init__(self, cred_dict):
        self.__cred_dict = cred_dict

    def __initialise_SQL_engine(self):
        cred = self.__cred_dict
        print("***************************")
        print("Attempting to connect to DB")
        engine = create_engine(
            f"{cred['RDS_DBTYPE']}+{cred['RDS_DBAPI']}://{cred['RDS_USER']}:{cred['RDS_PASSWORD']}@{cred['RDS_HOST']}:{cred['RDS_PORT']}/{cred['RDS_DATABASE']}")

        engine.connect()
        print("Connected Successfully")
        return engine

    def extract_rds_dataframe(self, table):
        engine = self.__initialise_SQL_engine()
        print(f"Finding SQL table: {table}")
        df = pd.read_sql_table(table, engine)
        return df

    @staticmethod
    def save_to_csv(df, name):
        pwd = os.getcwd()
        save_path = pwd + f"/dataset/{name}"
        print(f"Saving to CSV in dir: {save_path}")
        filepath = Path(save_path)
        df.to_csv(filepath)
        print("Completed Save")

    @staticmethod
    def csv_to_excel(file_name):
        pwd = os.getcwd()

        root_dataset_dir = pwd + '/dataset/'

        save_path = Path(f"{root_dataset_dir}/{file_name}.xlsx")
        print(f"Saving to excel in dir: {save_path}")

        read_file = pd.read_csv(pwd + f'/dataset/{file_name}.csv')
        read_file.to_excel(save_path, 'loan_data', header=True)
        print(f"Saving Complete")


if __name__ == "__main__":
    cred_dict = load_credentials()
    rds_con = RDSDatabaseConnector(cred_dict)

    df = rds_con.extract_rds_dataframe('loan_payments')

    RDSDatabaseConnector.save_to_csv(df, "loan_data.csv")
    RDSDatabaseConnector.csv_to_excel('loan_data')
