import missingno as msno
import pandas as pd
from scipy.stats import normaltest
from matplotlib import pyplot
from statsmodels.graphics.gofplots import qqplot
import plotly.express as px


class Plotter:
    def __init__(self, df):
        self.df = df

    # D’Agostino’s K^2 Test
    def agostino_k2_test(self, col):
        stat, p = normaltest(self.df[col], nan_policy='omit')
        print('Statistics=%.3f, p=%.3f' % (stat, p))

    # histogram
    def histogram(self, col):
        self.df[col].hist(bins=40)

    def qq_plot(self, col):
        self.df.sort_values(by=col, ascending=True)
        qq_plot = qqplot(self.df[col], scale=1, line='q')
        pyplot.show()

    def missing_nulls_vis(self):
        msno.matrix(self.df)
        pyplot.show()

    def correlated_vars(self, cols):
        df = self.df[cols]
        fig = px.imshow(df.corr(),
                        title="Correlation heatmap of Loan Data")
        fig.show()


if __name__ == '__main__':
    df = pd.read_csv('./dataset/formatted_loan_data.csv')
    plt = Plotter(df)

    # int rate has mostly normal distribution
    plt.agostino_k2_test('int_rate')
    print(df['int_rate'].median())
    plt.histogram('int_rate')
    plt.qq_plot('int_rate')

    # MCAR
    # 1. mths_since_last_major_derog   86.17 half of the data from vis is MCAR from cutoff point
    # 2. sub_grade is MCAR
    # 3. term is MCAR because loans must have terms and also its uncorrelated to other nulls missing vals from first look

    # NMAR
    # inq_last months
    # last_payment
    # collections_12_mths_ex_med
    # employment length
    # These values have no entry to signify no record eg. employment length = null because of no employment

    plt.missing_nulls_vis()
    # plt.correlated_vars(['mths_since_last_record',
    #                     'mths_since_last_delinq', 'mths_since_last_major_derog'])
