import pandas as pd
# from dateutil.parser import parse


class DataTransform:
    def __init__(self, df):
        self.df = df

    def string_to_boolean(self, col_name):
        mask = {'n': False, 'y': True}
        self.df[col_name].map(mask)
        print(self.df[col_name].unique())

    def cols_to_categories(self, array):
        for col in array:
            self.df[col] = self.df[col].astype('category')

    def strings_to_dates(self, array):
        for col in array:
            self.df[col] = pd.to_datetime(self.df[col], format="%b-%Y")

    def numerical_cols(self, cols):
        for col in cols:
            self.df[col] = self.df[col].str.extract('(\d+)')
            pd.to_numeric(self.df[col])

    def rename(self, col_name, new_col_name):
        self.df.rename(columns={col_name: new_col_name})

    def drop_cols(self, cols):
        for col in cols:
            self.df.drop(col, axis='columns')


if __name__ == '__main__':
    df = pd.read_csv('./dataset/loan_data.csv')
    Transformer = DataTransform(df)

    cols_to_drop = ['application_type', 'policy_code']

    Transformer.drop_cols(cols_to_drop)

    Transformer.string_to_boolean('payment_plan')

    categories = ['grade', 'sub_grade', 'home_ownership',
                  'verification_status', 'loan_status', 'purpose', 'term']

    Transformer.cols_to_categories(categories)

    string_dates = ['last_credit_pull_date', 'next_payment_date',
                    'last_payment_date', 'earliest_credit_line', 'issue_date']

    Transformer.strings_to_dates(string_dates)

    numerical_cols = ['employment_length', 'term']

    Transformer.rename('employment_length', 'Years Employed')
    Transformer.rename('term', 'Loan Months')

    Transformer.numerical_cols(numerical_cols)
