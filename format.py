import pandas as pd
from db_utils import RDSDatabaseConnector


class DataFormat:
    def __init__(self, df):
        self.df = df

    def string_to_boolean(self, col_name):
        mask = {'n': False, 'y': True}
        self.df[col_name].map(mask)
        self.df[col_name] = self.df[col_name].astype('bool')
        print(self.df[col_name].unique())

    def cols_to_categories(self, array):
        for col in array:
            self.df[col] = self.df[col].astype('category')

    def strings_to_dates(self, array):
        for col in array:
            self.df[col] = pd.to_datetime(self.df[col], format="%b-%Y")

    def extract_num_from_string(self, cols):
        for col in cols:
            self.df[col] = self.df[col].str.extract('(\d+)')

    def numerical_cols(self, cols):
        for col in cols:
            pd.to_numeric(self.df[col])

    def rename(self, col_name, new_col_name):
        self.df.rename(columns={col_name: new_col_name})

    def drop_cols(self, cols):
        for col in cols:
            self.df.drop(col, axis=1, inplace=True)

    def round_float(self, col, decimal_places):
        self.df[col] = self.df[col].apply(lambda x: round(x, decimal_places))

    # despite type coercsion we might want to convert explicitly if exporting to excel for cleanliness
    def to_int(self, cols):
        for col in cols:
            self.df[col] = self.df[col].fillna(0).astype('int32')


if __name__ == '__main__':
    df = pd.read_csv('./dataset/loan_data.csv')
    Transformer = DataFormat(df)

    # Convert n and y to bool values
    Transformer.string_to_boolean('payment_plan')

    categories = ['grade', 'sub_grade', 'home_ownership',
                  'verification_status', 'loan_status', 'purpose', 'employment_length']

    Transformer.cols_to_categories(categories)

    string_dates = ['last_credit_pull_date', 'next_payment_date',
                    'last_payment_date', 'earliest_credit_line', 'issue_date']

    Transformer.strings_to_dates(string_dates)

    # month and year terms to int
    string_to_num_cols = ['term']
    numerical_cols = ['term', 'mths_since_last_record',
                      'mths_since_last_major_derog', 'mths_since_last_delinq', 'mths_since_last_record']

    Transformer.rename('employment_length', 'Years Employed')
    Transformer.rename('term', 'Loan Months')

    Transformer.extract_num_from_string(string_to_num_cols)
    Transformer.numerical_cols(numerical_cols)

    # funded_amount seems to have more "nulls" according to .info() meaning that it has missing unexplained values that funded_amount_inv picks up on
    # application and policy code have all same values across whole column
    # out_prncp_inv/total_payment_inv is the same as out_prncp/total_payment
    drop_cols = ['funded_amount', 'application_type',
                 'policy_code', 'out_prncp_inv', 'total_payment_inv', 'Unnamed: 0', 'id']

    Transformer.drop_cols(drop_cols)

    # we don't convert these cols : 'mths_since_last_record', 'mths_since_last_major_derog' to int since they include 0 months since last to signify recent entry and null for NO entry
    Transformer.to_int(['term', 'open_accounts', 'total_accounts',
                       'collections_12_mths_ex_med', 'delinq_2yrs', 'loan_amount'])

    Transformer.round_float('collection_recovery_fee', 2)

    # decreases megabytes from 18.2 to 9.5
    # would be a lot more impactful in larger datasets
    print(Transformer.df.dtypes)
    print(Transformer.df.info())
    RDSDatabaseConnector.save_to_csv(Transformer.df, 'formatted_loan_data.csv')
