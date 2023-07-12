import matplotlib.pyplot as plt
import numpy as np

class interest_check(object):

    def __init__(self):
        self.bank_base_interest = .1/100
        self.interest_phase_1_target = 2.5/100
        self.set_interest_linear_parameters()
        self.set_index_model_parameters()
        self.calc_index()
        self.calc_interest()

    def interest_ripple(self, x):
        slope = (self.interest_phase_1_target - self.bank_base_interest) / (self.interest_ripple_start_year - self.interest_linear_years_offset)
        connection_point = self.bank_base_interest + slope * (self.interest_ripple_start_year - self.interest_linear_years_offset)
        return connection_point + self.interest_ripple_amp * np.sin((2 * np.pi / self.interrest_ripple_period) * x + self.interest_ripple_phase_shift)

    def set_interest_linear_parameters(self):
        self.interrest_ripple_period = 10
        self.interest_linear_years_offset = 3
        self.interest_ripple_start_year = 10
        self.interest_ripple_phase_shift = -2*np.pi*(self.interest_ripple_start_year//self.interrest_ripple_period)
        self.interest_ripple_amp = 0.5/100

    def set_index_model_parameters(self):
        self.current_index = -0.006
        self.target_index = 0.015
        self.years_span = 7
        self.index_rise_offset = 1


    def interest_linear(self, x):
        slope = (self.interest_phase_1_target - self.bank_base_interest) / (self.interest_ripple_start_year - self.interest_linear_years_offset)
        return slope * x - slope * self.interest_linear_years_offset + self.bank_base_interest

    def index_linear(self, x):
        slope = self.target_index / self.years_span
        return slope * x - slope * (self.years_span+self.index_rise_offset) + self.target_index


    def calc_interest(self):
        x = np.linspace(0, 30, 1000, dtype=np.float32)
        # self.bank_predicted_interest = np.piecewise(x, [x < 1, np.logical_and(1 <= x, x < 10), x >= 10], [0, self.interest_linear, self.interest_ripple])
        self.bank_predicted_interest = np.piecewise(x, [x <= self.interest_linear_years_offset,
                                                        np.logical_and(self.interest_linear_years_offset <= x, x < (self.interest_ripple_start_year)),
                                                        x >= (self.interest_ripple_start_year)],
                                                    [self.bank_base_interest, self.interest_linear, self.interest_ripple])

    def calc_index(self):
        x = np.linspace(0, 30, 1000, dtype=np.float32)
        self.index = np.piecewise(x, [x < self.index_rise_offset,
                                      np.logical_and(self.index_rise_offset <= x, x < (self.years_span+self.index_rise_offset)),
                                      x >= (self.years_span+self.index_rise_offset)],
                                  [self.current_index, self.index_linear, self.target_index])




if __name__ == '__main__':

    t = interest_check()
    #
    fig, ax = plt.subplots()
    ax.set_xticks(range(30))
    ax.plot(np.linspace(0, 30, 1000, dtype=np.float32), t.bank_predicted_interest, 'b', label='interest')
    ax.plot(np.linspace(0, 30, 1000, dtype=np.float32), t.index, 'r', label='index')
    leg = ax.legend()
    plt.show()






