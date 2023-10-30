import pandas as pd
import os


class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        return self.df.describe()

    def extract_statistics(self, columns):
        stats = {}
        for col in columns:
            print(f"Statistics for Col :{col}")
            stats[col] = {
                "median": self.df[col].median(),
                "std_dev": self.df[col].std(),
                "mean": self.df[col].mean()
            }
        return stats

    def distinct_values(self, cols):
        unique_values = {}
        for col in cols:
            print(f"Unique values for col: {col} \n")
            unique_values[col] = self.df[col].nunique()
        return unique_values

    def get_shape(self):
        print("Dataframe Shape: \n")
        return self.df.shape

    def percentage_null(self):
        return (self.df.isna().sum() * 100 / len(self.df)).to_frame(name="% Null")


def load_data(file_path):
    pwd = os.getcwd()
    df = pd.read_csv(pwd + file_path)
    return df


if __name__ == '__main__':
    df = load_data("/dataset/loan_data.csv")
    Info = DataFrameInfo(df)

    print(Info.extract_statistics(['loan_amount']))
    print(Info.distinct_values(['grade']))
    print(Info.get_shape())
    print(Info.percentage_null())
