import json
from typing import Callable, Iterator, Union, Optional, List
import matplotlib.pyplot as plt
import numpy as np


class Track(object):
    # Bank of israel prediction
    PRIME_ADDITION = 1.5 / 100
    BANK_BASE_INTEREST = .1 / 100
    INTEREST_PHASE_1_TARGET = 2.5 / 100

    # Interest model
    INTEREST_RIPPLE_PERIOD = 10
    INTEREST_LINEAR_YEARS_OFFSET = 3
    INTEREST_RIPPLE_START_YEAR = 10
    INTEREST_RIPPLE_PHASE_SHIFT = -2 * np.pi * (INTEREST_RIPPLE_START_YEAR // INTEREST_RIPPLE_PERIOD)
    INTEREST_RIPPLE_AMP = 0.5 / 100

    # Index model
    CURRENT_INDEX = 1.5/100
    # CURRENT_INDEX = -0.006
    TARGET_INDEX = 1.8/100
    YEARS_SPAN = 7
    INDEX_RISE_OFFSET = 0

    def __init__(self,
                 months: int = 0,
                 amount: float = 0,
                 interest: float = None,
                 index: float = 0,
                 name: str = "",
                 interest_model: str = 'const',
                 index_model: str = 'const',
                 early_closure: tuple = None,
                 interest_yearly_addition_every_five=1
                 ):

        self.months = int(months)
        self.current_amount = amount
        self.initial_amount = amount
        self.initial_interest = interest / 100 / 12 if interest is not None else 0
        self.initial_index = index / 100 / 12
        self.name = name
        self.interest_model = interest_model
        self.index_model = index_model
        self.early_closure = (self.months, -1) if early_closure is None else early_closure  # Month, amount

        self._index = None
        self._interest = None

        self.bank_predicted_anchor = None
        self.interest_yearly_addition_every_five = interest_yearly_addition_every_five

        self.principal_coverage_list = []
        self.interest_payments_list = []
        self.monthly_return_list = []
        self.current_amounts_list = []
        self.index_payments_list = []
        self.current_amount_when_early_closing = None

        self.calc_interest()
        self.calc_index()
        self.calc_track_stats()

    def interest_ripple(self, x):
        slope = (self.INTEREST_PHASE_1_TARGET - self.BANK_BASE_INTEREST) / (self.INTEREST_RIPPLE_START_YEAR - self.INTEREST_LINEAR_YEARS_OFFSET)
        connection_point = self.BANK_BASE_INTEREST + slope * (self.INTEREST_RIPPLE_START_YEAR - self.INTEREST_LINEAR_YEARS_OFFSET)
        return connection_point + self.INTEREST_RIPPLE_AMP * np.sin((2 * np.pi / self.INTEREST_RIPPLE_PERIOD) * x + self.INTEREST_RIPPLE_PHASE_SHIFT)

    def interest_linear(self, x):
        slope = (self.INTEREST_PHASE_1_TARGET - self.BANK_BASE_INTEREST) / (self.INTEREST_RIPPLE_START_YEAR - self.INTEREST_LINEAR_YEARS_OFFSET)
        return slope * x - slope * self.INTEREST_LINEAR_YEARS_OFFSET + self.BANK_BASE_INTEREST

    def index_linear(self, x):
        slope = (self.TARGET_INDEX  - self.CURRENT_INDEX)/ self.YEARS_SPAN
        return slope * x - slope * (self.YEARS_SPAN+self.INDEX_RISE_OFFSET) + self.TARGET_INDEX


    def calc_interest(self):
        if self.interest_model == 'npv_prime':
            x = np.arange(0, 30, dtype=np.float32)
            self.bank_predicted_anchor = \
                np.piecewise(x, [x <= self.INTEREST_LINEAR_YEARS_OFFSET,
                                 np.logical_and(self.INTEREST_LINEAR_YEARS_OFFSET <= x, x < self.INTEREST_RIPPLE_START_YEAR),
                                 x >= self.INTEREST_RIPPLE_START_YEAR],
                             [self.BANK_BASE_INTEREST, self.interest_linear, self.interest_ripple]
                             )
            prime_interest = self.bank_predicted_anchor + self.PRIME_ADDITION
            self._interest = np.repeat(prime_interest/12, 12)[:self.months] - (prime_interest[0]/12 - self.initial_interest)

        elif self.interest_model == 'finwiz_prime':
            with open(r"interests\intereset_Prime_finwiz.json", 'r') as json_reader:
                prime_interest_pred = json.load(json_reader)
                self.bank_predicted_anchor = np.array([float(point['y'])/(100*12) for point in prime_interest_pred['data']])
                addition_to_acnchor = self.initial_interest - self.bank_predicted_anchor[0]

                prime_interest = self.bank_predicted_anchor + addition_to_acnchor
                # prime_interest = self.bank_predicted_anchor + self.PRIME_ADDITION/12
                self._interest = prime_interest

        elif self.interest_model == 'finwiz_changing_w_index':
            with open(r"interests\intereset_W_CPI_finwiz.json", 'r') as json_reader:
                changing_w_index_pred = json.load(json_reader)
                self.bank_predicted_anchor = np.array([float(point['y'])/(100*12) for point in changing_w_index_pred['data']])
                addition_to_acnchor = self.initial_interest - self.bank_predicted_anchor[0]
                self._interest = np.repeat(self.bank_predicted_anchor + addition_to_acnchor, 12*5).tolist()

        elif self.interest_model == 'finwiz_changing_wo_index':
            with open(r"interests\intereset_WO_CPI_finwiz.json", 'r') as json_reader:
                changing_wo_index_pred = json.load(json_reader)
                self.bank_predicted_anchor = np.array([float(point['y'])/(100*12) for point in changing_wo_index_pred['data']])
                addition_to_acnchor = self.initial_interest - self.bank_predicted_anchor[0]
                self._interest = np.repeat(self.bank_predicted_anchor + addition_to_acnchor, 12*5).tolist()


        elif self.interest_model == 'const':
            self._interest = [self.initial_interest] * self.months if not isinstance(self.initial_interest, list) else self.initial_interest
        else:
            self._interest = [self.initial_interest + (self.interest_yearly_addition_every_five / 100 / 12) * i for i in range(int(np.ceil(self.months / (12 * 5)))) for _ in range(12 * 5)] if not isinstance(self.initial_interest, list) else self.initial_interest
            # print(self.name, self.months, len(self._interest))

    def calc_index(self):
        if self.index_model == 'npv_index':
            x = np.arange(-1, 30, dtype=np.float32)
            index = np.piecewise(x, [x <= self.INDEX_RISE_OFFSET,
                                     np.logical_and(self.INDEX_RISE_OFFSET < x, x < (self.YEARS_SPAN + self.INDEX_RISE_OFFSET)),
                                     x >= (self.YEARS_SPAN + self.INDEX_RISE_OFFSET)],
                                 [self.CURRENT_INDEX, self.index_linear, self.TARGET_INDEX]
                                 )

            self._index = np.repeat(index/12, 12)[:self.months]
        elif self.index_model == 'finwiz_index':
            with open(r"interests\inflation_finwiz.json", 'r') as json_reader:
                inflation_pred = json.load(json_reader)
                index = np.array([float(point['y'])/(100*12) for point in inflation_pred['data']])
                self._index = index
        elif self.index_model == 'const':
            self._index = [self.initial_index] * self.months if not isinstance(self.initial_index, list) else self.initial_index
        else:
            self._index = [0] * self.months
        # Avoiding deflation
        index_array = np.array(self._index)
        index_array[index_array < 0] = 0
        self._index = index_array.tolist()


    @property
    def interest(self):
        return self._interest

    @property
    def index(self):
        return self._index

    def calc_month_return(self, month):
        months_left = self.months - month
        month_return = self.current_amount * (self.interest[month] * (self.interest[month] + 1) ** months_left) /\
                       ((self.interest[month] + 1) ** months_left - 1)
        self.monthly_return_list.append(month_return)
        return month_return

    def apply_index(self, month):
        index_payment = self.current_amount * self.index[month]
        self.current_amount += index_payment
        self.index_payments_list.append(index_payment)

    def calc_interest_payed_and_principal_covered(self, month, month_return):
        interest_payments = self.interest[month] * self.current_amount
        principal_coverage = month_return - interest_payments
        self.current_amount -= principal_coverage
        self.current_amounts_list.append(self.current_amount)
        self.interest_payments_list.append(interest_payments)
        self.principal_coverage_list.append(principal_coverage)


    def calc_track_stats(self):
        # https://www.businessinsider.com/personal-finance/how-to-calculate-mortgage-payment

        for month in range(self.months):
            if self.early_closure[0] == month:
                closure_amount = self.early_closure[1]
                self.current_amount_when_early_closing = int(self.current_amount)
                self.current_amount = self.current_amount - closure_amount if closure_amount != -1 else 0
                break
            self.apply_index(month)
            month_return = self.calc_month_return(month)
            self.calc_interest_payed_and_principal_covered(month, month_return)

    def get_monthly_return_list(self):
        return self.monthly_return_list

    def get_principal_coverage_list(self):
        return self.principal_coverage_list

    def get_index_payments_list(self):
        return self.index_payments_list

    def get_interest_payments_list(self):
        return self.interest_payments_list

    def get_current_principal_list(self):
        return self.current_amounts_list

    def get_return_rate(self):
        return sum(self.monthly_return_list) / self.initial_amount

    def get_mean_life_span(self):
        cumsum = np.cumsum(self.monthly_return_list)
        mean_life_span_month = np.abs(cumsum - cumsum[-1] / 2).argmin()
        return mean_life_span_month

    def __len__(self):
        return self.months

    def __str__(self):
        initial_amount = self.initial_amount
        min_monthly_return = min(self.monthly_return_list)
        max_monthly_return = max(self.monthly_return_list)
        total_interest_payed = sum(self.interest_payments_list)
        total_index_payments = sum(self.index_payments_list)
        final_return = sum(self.monthly_return_list)
        return_rate = self.get_return_rate()
        printed_str = "initial_amount: {} " \
                      "min_monthly_return: {} " \
                      "max_monthly_return: {} " \
                      "total_interest_payed: {} " \
                      "total_index_payments: {} " \
                      "final_return: {}" \
                      "return rate: {}"


        printed_str = self.name + "\n" + "="*len(self.name) + "\n"
        printed_str += "ריבית שנתית: {}\n" \
                       "סך הלוואה: {}\n" \
                      "החזר חודשי מינימאלי: {}\n" \
                      "החזר חודשי מקסימלי: {}\n" \
                      "החזר ריבית: {}\n" \
                      "החזר הצמדת מדד: {}\n" \
                      "החזר בסוף תקופה: {}\n" \
                      "יחס החזר: {}\n" \
                       "\n"

        return printed_str.format(np.round(self.initial_interest * 12 * 100, 3),
                                  int(initial_amount),
                                  int(min_monthly_return),
                                  int(max_monthly_return),
                                  int(total_interest_payed),
                                  int(total_index_payments),
                                  int(final_return),
                                  np.round(return_rate, 2)
                                  )


if __name__ == '__main__':

    yearly_interest_percent = 2
    yearly_index_percent = 0.6
    loan_amount = 1.05e6 * 0.4
    loan_years = 25

    loan_months = 12 * loan_years
    t = Track(months=loan_months,
               amount=loan_amount,
               interest=yearly_interest_percent,
               index=yearly_index_percent,
               name="prime",
               interest_model='npv_prime',
               index_model='npv_index'
               )

    print(t.get_mean_life_span())
    print(t)
    fig, ax = plt.subplots()
    ax.plot(np.array(range(len(t.interest))), [i*100*12 for i in t.interest], 'b', label='interest')
    ax.plot(np.array(range(len(t.index))), [i*100*12 for i in t.index], 'r', label='index')
    # ax.plot(np.array(range(t.months)), t.get_monthly_return_list(), 'r', label='Monthly return')
    # ax.plot(np.array(range(t.months)), t.get_current_principal_list(), 'b', label='Principal list')
    # ax.plot(np.array(range(len(t.index)))/12, [i*100*12 for i in t.index], 'r', label='index')
    leg = ax.legend()
    plt.show()

