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
        self.cred_dict = cred_dict

    def initialise_SQL_engine(self):
        cred = self.cred_dict
        print("*************************************************************")
        print("Attempting to connect to DB")
        engine = create_engine(
            f"{cred['RDS_DBTYPE']}+{cred['RDS_DBAPI']}://{cred['RDS_USER']}:{cred['RDS_PASSWORD']}@{cred['RDS_HOST']}:{cred['RDS_PORT']}/{cred['RDS_DATABASE']}")

        engine.connect()
        print("Connected Successfully")
        return engine

    def extract_rds_dataframe(self, engine):
        df = pd.read_sql_table('loan_payments', engine)
        print(df.head())
        return df

    def save_to_csv(self, df, name):
        pwd = os.getcwd()
        filepath = Path(pwd + f"/dataset/{name}")
        df.to_csv(filepath)


cred_dict = load_credentials()
rds_con = RDSDatabaseConnector(cred_dict)

engine = rds_con.initialise_SQL_engine()

df = rds_con.extract_rds_dataframe(engine)

rds_con.save_to_csv(df, "loan_data")
