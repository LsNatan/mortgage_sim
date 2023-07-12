from collections import OrderedDict
from copy import deepcopy
import datetime
import random
import fastrand

import numpy as np
import scipy.optimize as opt
from scipy.special import softmax

from track import Track
from mix import Mix
from interest_excel_parser import InterestExcelParser



class MortgageSimulator(object):
    def __init__(self,
                 total_loan=None,
                 index=None,
                 funding_percentage=None,
                 max_monthly_return=None,
                 interest_rates_joint_index_excel=None,
                 interest_rates_not_joint_index_excel=None,
                 ):
        self.total_loan = total_loan
        self.index = index
        self.max_monthly_return = max_monthly_return
        self.funding_percentage = funding_percentage
        self.interest_rates_joint_index = InterestExcelParser(interest_rates_joint_index_excel)
        self.interest_rates_not_joint_index = InterestExcelParser(interest_rates_not_joint_index_excel)

        self.tested_mix = None

    @property
    def max_amount_prime_track(self):
        return self.total_loan/3

    @property
    def min_amount_constant_interest_track(self):
        return self.total_loan * .3

    def function_to_be_optimized(self, x):
        # print("OPT!")
        # print(x)

        track1_funding = x[0]
        track1_duration = int(x[1])
        track2_funding = x[2]
        track2_duration = int(x[3])
        track3_funding = x[4]
        track3_duration = int(x[5])
        track4_funding = x[6]
        track4_duration = int(x[7])
        track5_funding = x[8]
        track5_duration = int(x[9])

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
                              interest_rates_not_joint_index_excel=self.interest_rates_not_joint_index
                              )

        return self.tested_mix.return_rate, self.tested_mix.mix_max_monthly_return
        # return self.tested_mix.return_rate, self.tested_mix.mix_max_monthly_return

    def genetic(self):

        def gen_parent():
            track1_funding = 1./4
            track1_duration = 20
            track2_funding = 1./4
            track2_duration = 20  # Minimum legal
            track3_funding = 1./5
            track3_duration = 20
            track4_funding = 1./4
            track4_duration = 20  # Minimum legal
            track5_funding = 1./4
            track5_duration = 20

            return np.array([track1_funding,
                             track1_duration,
                             track2_funding,
                             track2_duration,
                             track3_funding,
                             track3_duration,
                             track4_funding,
                             track4_duration,
                             track5_funding,
                             track5_duration
                             ])


        def get_fitness(x):
            return_rate, mix_max_monthly_return = self.function_to_be_optimized(x)

            # index = sum([t.get_accompanying_payments() for t in self.tested_mix.tracks])
            # return_rate_importance = .9
            fitness = 1. / (return_rate**(1./3) * (mix_max_monthly_return)**(1./2))
            # fitness = 1. / (return_rate * np.log(abs(mix_max_monthly_return - self.max_monthly_return + 1e-6)))
            return fitness, mix_max_monthly_return, return_rate

        def mutate(parent):

            while True:
                index = fastrand.pcg32bounded(len(parent))
                # index = random.randrange(0, len(parent))
                childGenes = deepcopy(parent)
                if index % 2 == 0:
                    newGen = (fastrand.pcg32bounded(5*2+1) - 5) / 100
                    # newGen = random.randint(-50, 50) / 100
                    # newGen = random.choices([-.02, .02])
                    # newGen = random.uniform(-.5, .5)
                    # weights = [t.get_accompanying_payments() for t in self.tested_mix.tracks]
                    # weights /= sum(weights)

                    complementary = fastrand.pcg32bounded(11)//2
                    # complementary = random.choices(range(0, 10, 2))[0]
                    if not(complementary != index and
                            0 < (childGenes[index]+newGen) < 1 and
                            0 < (childGenes[complementary]-newGen) < 1):
                        continue

                    childGenes[index] += newGen
                    childGenes[complementary] -= newGen



                    # sofmaxed = softmax(childGenes[::2] * weights)
                    # for i in range(0, 5):
                    #     childGenes[2*i] = sofmaxed[i]

                    if childGenes[0] > 1./3 or (childGenes[6] + childGenes[8]) < 0.3:
                        continue
                else:
                    newGen = fastrand.pcg32bounded(2*2+1) - 2
                    # newGen = random.randint(-15, 15)
                    new_duration = childGenes[index] + newGen
                    if 4 > new_duration or new_duration > 30:
                        continue
                    else:
                        childGenes[index] += newGen

                # print( get_fitness(childGenes))
                break
            return childGenes


        def display(guess):
            # timeDiff = datetime.datetime.now() - startTime
            fitness, mix_max_monthly_return, return_rate = get_fitness(guess)
            print("{}\t{}\t{}\t{}\t{}".format(guess.tolist(),
                                              return_rate, fitness,
                                              mix_max_monthly_return,
                                              self.tested_mix.mix_total_monthly_return - self.total_loan))
            # print(self.tested_mix)
            # print("{}\t{}\t{}".format(guess, fitness, timeDiff))


        bestParent = gen_parent()
        bestFitness, mix_max_monthly_return, return_rate = get_fitness(bestParent)
        display(bestParent)

        fitness_trials = OrderedDict()
        total_trials = 0
        diff_trials = 0
        while True:
            child = mutate(bestParent)
            childFitness, mix_max_monthly_return, return_rate = get_fitness(child)
            if bestFitness >= childFitness:
                total_trials += 1
                diff_trials += 1
                # print(child.tolist(), childFitness, mix_max_monthly_return)
                continue
            # print(bestFitness, childFitness, bestFitness > childFitness)
            display(child)

            bestFitness = childFitness
            bestParent = child
            fitness_trials[bestFitness] = diff_trials
            diff_trials = 0



    # def function_to_be_optimized(self, x):
    #     # print("OPT!")
    #     # print(x)
    #
    #     track1_funding = x[0]/100
    #     track1_duration = int(x[1])
    #     track2_funding = x[2]/100
    #     track2_duration = int(x[3])
    #     track3_funding = x[4]/100
    #     track3_duration = int(x[5])
    #     track4_funding = x[6]/100
    #     track4_duration = int(x[7])
    #     track5_funding = x[8]/100
    #     track5_duration = int(x[9])
    #
    #     t1_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, "prime")
    #     t2_interest = self.interest_rates_joint_index.query_percentage(self.funding_percentage, "changing every five")
    #     t3_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, "changing every five")
    #     t4_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, track4_duration)
    #     t5_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, track5_duration)
    #
    #     track1_amount = track1_funding * self.total_loan
    #     track2_amount = track2_funding * self.total_loan
    #     track3_amount = track3_funding * self.total_loan
    #     track4_amount = track4_funding * self.total_loan
    #     track5_amount = track5_funding * self.total_loan
    #
    #     t1 = Track(months=track1_duration * 12, amount=track1_amount, interest=t1_interest, index=self.index, name="prime")
    #     t2 = Track(months=track2_duration * 12, amount=track2_amount, interest=t2_interest, index=self.index, name="changing every five joint to index")
    #     t3 = Track(months=track3_duration * 12, amount=track3_amount, interest=t3_interest, index=self.index, name="changing every five not joint to index")
    #     t4 = Track(months=track4_duration * 12, amount=track4_amount, interest=t4_interest, index=self.index, name="constant interest joint to index")
    #     t5 = Track(months=track5_duration * 12, amount=track5_amount, interest=t5_interest, index=self.index, name="constant interest not joint to index")
    #
    #     self.tested_mix = Mix([t1, t2, t3, t4, t5], "my mix")
    #
    #     return self.tested_mix.return_rate


    def monthly_return_constraint(self, x):
        # print("CONST!")
        track1_funding = x[0]/100
        track1_duration = int(x[1])
        track2_funding = x[2]/100
        track2_duration = int(x[3])
        track3_funding = x[4]/100
        track3_duration = int(x[5])
        track4_funding = x[6]/100
        track4_duration = int(x[7])
        track5_funding = x[8]/100
        track5_duration = int(x[9])

        t1_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, "prime")
        t2_interest = self.interest_rates_joint_index.query_percentage(self.funding_percentage, "changing every five")
        t3_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, "changing every five")
        t4_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, track4_duration)
        t5_interest = self.interest_rates_not_joint_index.query_percentage(self.funding_percentage, track5_duration)

        track1_amount = track1_funding * self.total_loan
        track2_amount = track2_funding * self.total_loan
        track3_amount = track3_funding * self.total_loan
        track4_amount = track4_funding * self.total_loan
        track5_amount = track5_funding * self.total_loan

        t1 = Track(months=track1_duration*12, amount=track1_amount, interest=t1_interest, index=self.index, name="prime")
        t2 = Track(months=track2_duration*12, amount=track2_amount, interest=t2_interest, index=self.index, name="changing every five joint to index")
        t3 = Track(months=track3_duration*12, amount=track3_amount, interest=t3_interest, index=self.index, name="changing every five not joint to index")
        t4 = Track(months=track4_duration*12, amount=track4_amount, interest=t4_interest, index=self.index, name="constant interest joint to index")
        t5 = Track(months=track5_duration*12, amount=track5_amount, interest=t5_interest, index=self.index, name="constant interest not joint to index")

        experemental_mix = Mix([t1, t2, t4, t5], "my mix")
        # experemental_mix = Mix([t1, t2, t3, t4, t5], "my mix")

        return -experemental_mix.mix_max_monthly_return + self.max_monthly_return



    @property
    def bounds(self):
        return (0, 1./3)*100, (4, 30), (0, 1)*100, (4, 30), (0, 1)*100, (4, 30), (0, 1)*100, (4, 30), (0.3, 1)*100, (4, 30)

    @property
    def initial_conditions(self):
        track1_funding = 1./3
        track1_duration = 21
        track2_funding = 0
        track2_duration = 4  # Minimum legal
        track3_funding = 1./3
        track3_duration = 20
        track4_funding = 0
        track4_duration = 4  # Minimum legal
        track5_funding = 1./3
        track5_duration = 18.3

        track1_funding = 1./4 * 100
        track1_duration = 20
        track2_funding = 1./4 * 100
        track2_duration = 20  # Minimum legal
        # track3_funding = 1./5 * 100
        # track3_duration = 20
        track4_funding = 1./4 * 100
        track4_duration = 20  # Minimum legal
        track5_funding = 1./4 * 100
        track5_duration = 20

        return np.array([track1_funding,
                         track1_duration,
                         track2_funding,
                         track2_duration,
                         track3_funding,
                         track3_duration,
                         track4_funding,
                         track4_duration,
                         track5_funding,
                         track5_duration
                         ])

    def get_optimization_constaraints_dict(self):
        cons = [{'type': 'eq', 'fun': lambda x: x[0] + x[2] + x[4] + x[6] + x[8] - 1},
                {'type': 'ineq', 'fun': self.monthly_return_constraint},
                ]
        return cons

    def optimize(self):
        const = self.get_optimization_constaraints_dict()
        options = {'disp': True,
                   'initial_tr_radius': 1,
                   'factorization_method': 'SVDFactorization',
                   }
        res = opt.minimize(self.function_to_be_optimized,
                           self.initial_conditions,
                           method='trust-constr',
                           bounds=self.bounds,
                           constraints=const,
                           options=options
                           )
        return res

if __name__ == '__main__':
    excel_path_joint = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\joint.xlsx"
    excel_path_not_joint = r"C:\Users\dp26422\PycharmProjects\mortgage\interests\not_joint.xlsx"
    total_loan = 1.1e6
    index = .7
    max_monthly_return = 6.5e3
    funding_percentage = 60
    ms = MortgageSimulator(total_loan,
                           index,
                           funding_percentage,
                           max_monthly_return,
                           excel_path_joint,
                           excel_path_not_joint
                           )
    # res = ms.optimize().x
    # print(res)
    # print(ms.function_to_be_optimized(ms.initial_conditions))


    random.seed()
    startTime = datetime.datetime.now()
    ms.genetic()






