from db_utils import load_data


class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        return self.df.dtypes

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
        return round((self.df.isna().sum() * 100 / len(self.df)), 2).to_frame(name="% Null")


if __name__ == '__main__':
    df = load_data("/dataset/formatted_loan_data.csv")
    Info = DataFrameInfo(df)

    print(Info.extract_statistics(['loan_amount']))
    print(Info.distinct_values(['grade']))
    print(Info.get_shape())
    print(Info.percentage_null())
    print(Info.describe_columns())
    print(Info.extract_statistics(['mths_since_last_major_derog']))
