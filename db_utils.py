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
        print(df.head())
        return df

    @staticmethod
    def save_to_csv(df, name):
        pwd = os.getcwd()
        save_path = pwd + f"/dataset/{name}"
        print(f"Saving to CSV in dir: {save_path}")
        filepath = Path(save_path)
        df.to_csv(filepath)
        print("Completed Save")


if __name__ == "__main__":
    cred_dict = load_credentials()
    rds_con = RDSDatabaseConnector(cred_dict)

    df = rds_con.extract_rds_dataframe('loan_payments')

    RDSDatabaseConnector.save_to_csv(df, "loan_data.csv")
