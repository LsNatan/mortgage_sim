import pandas as pd
import numpy as np
from scipy import interpolate


class InterestPrognosisExcelParser(object):
    def __init__(self, excel_path):
        self.excel_path = excel_path

        self.interpolator = None

        self.df = pd.read_excel(open(self.excel_path, 'rb'))
        self.create_prognosis_interpolator()

    def create_prognosis_interpolator(self):
        self.df = self.df.loc[self.df['average type'] == 'קלנדרי']
        latest_prognossis = self.df.iloc[[len(self.df) - 1]].filter(regex='years')
        prognosis_years = latest_prognossis.columns.str.extract(r'(\d+)').values.ravel()
        x = prognosis_years.astype(float)
        y = latest_prognossis.values.ravel()
        self.interpolator = interpolate.interp1d(x, y, kind='linear')

    def get_prognosis_diff(self, years, min_statistics_year, method='mean'):
        # years = 5
        # min_statistics_year = 2015
        min_statistics_year_df = self.df.loc[pd.DatetimeIndex(self.df['year']).year >= min_statistics_year]
        years_prognosis = min_statistics_year_df['{} years'.format(years)].values
        diff = np.diff(years_prognosis)
        if method == 'mean':
            return np.mean(diff)
        elif method == 'median':
            return np.median(diff)
        else:
            pass

    def get_latest_prognosis(self, years, min_statistics_year):
        # years = 5
        # min_statistics_year = 2015
        min_statistics_year_df = self.df.loc[pd.DatetimeIndex(self.df['year']).year >= min_statistics_year]
        years_prognosis = min_statistics_year_df['{} years'.format(years)].values
        return years_prognosis[-1]

    def get_prognosis(self, year):
        return self.interpolator(year).ravel()[0]


if __name__ == '__main__':
    excel_path = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\joint_interest_prognosis_processed.xls"
    p = InterestPrognosisExcelParser(excel_path)
    print(p.get_prognosis(6))
