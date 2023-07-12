import optuna

from track import Track
from mix import Mix
from interest_excel_parser import InterestExcelParser

# Define an objective function to be minimized.


class MortgageSimulator(object):
    def __init__(self,
                 total_loan=None,
                 index=None,
                 funding_percentage=None,
                 max_monthly_return=None,
                 interest_rates_joint_index_excel=None,
                 interest_rates_not_joint_index_excel=None,
                 interest_rates_prognosis_joint_index_excel=None,
                 interest_rates_prognosis_not_joint_index_excel=None,
                 trial=None
                 ):
        self.total_loan = total_loan
        self.index = index
        self.max_monthly_return = max_monthly_return
        self.funding_percentage = funding_percentage
        self.interest_rates_joint_index = InterestExcelParser(interest_rates_joint_index_excel)
        self.interest_rates_not_joint_index = InterestExcelParser(interest_rates_not_joint_index_excel)
        self.interest_rates_prognosis_joint_index_excel = interest_rates_prognosis_joint_index_excel
        self.interest_rates_prognosis_not_joint_index_excel = interest_rates_prognosis_not_joint_index_excel

        self.trial = trial
        self.tested_mix = None

    @property
    def max_amount_prime_track(self):
        return self.total_loan/3

    @property
    def min_amount_constant_interest_track(self):
        return self.total_loan * .3

    def create_mix(self):

        track1_funding = self.trial.suggest_int('track1_funding', 0, 100/3)
        track1_duration = self.trial.suggest_int('track1_duration', 4, 30)
        track2_funding = self.trial.suggest_int('track2_funding', 0, 100-track1_funding)
        track2_duration = self.trial.suggest_int('track2_duration', 4, 30)
        track3_funding = self.trial.suggest_int('track3_funding', 0, 100-track1_funding-track2_funding)
        track3_duration = self.trial.suggest_int('track3_duration', 4, 30)
        track4_funding = self.trial.suggest_int('track4_funding', 0, 100-track1_funding-track2_funding-track3_funding)
        track4_duration = self.trial.suggest_int('track4_duration', 4, 30)
        track5_funding = self.trial.suggest_int('track5_funding', 0, 100-track1_funding-track2_funding-track3_funding-track4_funding)
        track5_duration = self.trial.suggest_int('track5_duration', 4, 30)

        t1_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, "prime")
        t2_interest = self.interest_rates_joint_index.query_percentage(self.funding_percentage, "changing")
        t3_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, "changing")
        t4_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, track4_duration)
        t5_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, track5_duration)

        track1_amount = track1_funding * self.total_loan
        track2_amount = track2_funding * self.total_loan
        track3_amount = track3_funding * self.total_loan
        track4_amount = track4_funding * self.total_loan
        track5_amount = track5_funding * self.total_loan

        t1 = Track(months=track1_duration * 12, amount=track1_amount, interest=t1_interest, interest_model='model', index=self.index, index_model='model', name="prime")
        t2 = Track(months=track2_duration * 12, amount=track2_amount, interest=t2_interest, interest_model='change', index=self.index, index_model='model', name="changing every five joint to index")
        t3 = Track(months=track3_duration * 12, amount=track3_amount, interest=t3_interest, interest_model='change', index=self.index, index_model='model', name="changing every five not joint to index")
        t4 = Track(months=track4_duration * 12, amount=track4_amount, interest=t4_interest, interest_model='const', index=self.index, index_model='model', name="constant interest joint to index")
        t5 = Track(months=track5_duration * 12, amount=track5_amount, interest=t5_interest, interest_model='const', index=self.index, index_model='model', name="constant interest not joint to index")

        self.tested_mix = Mix(
                              # [t1, t2, t4, t5],
                              [t1, t2, t3, t4, t5],
                              "my mix",
                              interest_rates_joint_index_excel=self.interest_rates_joint_index,
                              interest_rates_not_joint_index_excel=self.interest_rates_not_joint_index,
                              interest_rates_prognosis_joint_index_excel=self.interest_rates_prognosis_joint_index_excel,
                              interest_rates_prognosis_not_joint_index_excel=self.interest_rates_prognosis_not_joint_index_excel
                              )

    def caluclate_goodness(self):
        return 1./(self.tested_mix.return_rate * self.tested_mix.mix_max_monthly_return)




def objective(trial):

    # Invoke suggest methods of a Trial object to generate hyperparameters.
    excel_path_joint = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\joint.xlsx"
    excel_path_not_joint = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\not_joint.xlsx"
    interest_rates_prognosis_joint_index_excel = r"interests/joint_interest_prognosis_processed.xls"
    interest_rates_prognosis_not_joint_index_excel = r"interests/not_joint_interest_prognosis_processed.xls"

    total_loan = 1.1e6
    index = .7
    max_monthly_return = 6.5e3
    funding_percentage = 60
    ms = MortgageSimulator(total_loan,
                           index,
                           funding_percentage,
                           max_monthly_return,
                           excel_path_joint,
                           excel_path_not_joint,
                           interest_rates_prognosis_joint_index_excel,
                           interest_rates_prognosis_not_joint_index_excel,
                           trial
                           )

    ms.create_mix()
    goodness = ms.caluclate_goodness()
    return goodness # An objective value linked with the Trial object.


study = optuna.create_study()  # Create a new study.
study.optimize(objective, n_trials=1000)  # s optimization of the objective function.