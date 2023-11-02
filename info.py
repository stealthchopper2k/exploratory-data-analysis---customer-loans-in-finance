from db_utils import load_data
from tabulate import tabulate


class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        return self.df.dtypes

    def extract_statistics(self, columns):
        for col in columns:
            print(f"Statistics for Col :{col}")
            return self.df[col].describe()

    def skew_data(self, cols):
        skew_data = []
        for col in cols:
            skew_value = self.df[col].skew()
            skew_data.append([col, skew_value])

        print(tabulate(skew_data, headers=[
              "Column", "Skewness"], tablefmt="pretty"))

    def distinct_values(self, cols):
        unique_values = {}
        for col in cols:
            print(f"Unique values for col: {col} \n")
            unique_values[col] = self.df[col].nunique()
        return unique_values

    def get_shape(self):
        print("Dataframe Shape:")
        return self.df.shape

    def percentage_null(self):
        null_percentages = (self.df.isna().sum() * 100 /
                            len(self.df)).to_frame(name="% Null")
        non_zero_null_percentages = null_percentages[null_percentages["% Null"] > 0]
        return non_zero_null_percentages


if __name__ == '__main__':
    df = load_data("/dataset/formatted_loan_data.csv")
    Info = DataFrameInfo(df)

    print(Info.extract_statistics(['loan_amount']))
    print(Info.distinct_values(['grade']))
    print(Info.get_shape())
    print(Info.percentage_null())
    print(Info.describe_columns())
    print(Info.extract_statistics(['mths_since_last_major_derog']))
