import missingno as msno
import pandas as pd
from scipy.stats import normaltest
from matplotlib import pyplot
from statsmodels.graphics.gofplots import qqplot
import seaborn as sns
import numpy as np


class Plotter:
    def __init__(self, df):
        self.df = df

    # D’Agostino’s K^2 Test
    def agostino_k2_test(self, col):
        stat, p = normaltest(self.df[col], nan_policy='omit')
        print('Statistics=%.3f, p=%.3f' % (stat, p))

    # histogram
    def skewed_cols(self, num_cols):
        sns.set(font_scale=0.7)
        f = pd.melt(self.df, value_vars=num_cols)
        g = sns.FacetGrid(f, col="variable", col_wrap=3,
                          sharex=False, sharey=False)
        g = g.map(sns.histplot, "value", kde=True)
        pyplot.show()

    def qq_plot(self, col):
        self.df.sort_values(by=col, ascending=True)
        qq_plot = qqplot(self.df[col], scale=1, line='q')
        pyplot.show()

    def missing_nulls_vis(self):
        msno.matrix(self.df)
        pyplot.show()

    def correlated_vars(self, cols):
        corr = self.df[cols].corr()
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True

        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        sns.heatmap(corr, mask=mask, square=True, linewidths=5,
                    annot=False, cmap=cmap)

        pyplot.show()


if __name__ == '__main__':
    df = pd.read_csv('./dataset/formatted_loan_data.csv')
    plt = Plotter(df)

    # int rate has mostly normal distribution
    # plt.agostino_k2_test('int_rate')
    # print(df['int_rate'].median())
    # plt.histogram('int_rate')
    # plt.qq_plot('int_rate')

    plt.missing_nulls_vis()
    # small visible correlation between interest rate, term and loan
    # there is small correlation between missing numerical cols

    numerical_cols = ['loan_amount',
                      'funded_amount_inv', 'int_rate', 'instalment', 'dti', 'total_payment', 'total_accounts', 'mths_since_last_major_derog', 'collections_12_mths_ex_med', 'recoveries', 'open_accounts', 'annual_inc']

    plt.correlated_vars(numerical_cols)

    plt.skewed_cols(numerical_cols)
