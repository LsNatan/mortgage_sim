import os

import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter

from track import Track
from interest_excel_parser import InterestExcelParser
from interest_prognosis_excel_parser import InterestPrognosisExcelParser



class Mix(object):
    def __init__(self,
                 tracks,
                 name="",
                 excel_path=None,
                 interest_rates_joint_index_excel=None,
                 interest_rates_not_joint_index_excel=None,
                 interest_rates_prognosis_joint_index_excel=None,
                 interest_rates_prognosis_not_joint_index_excel=None

                 ):
        self.tracks = tracks
        self.name = name

        self.excel_cell_width_margin = 3
        self.excel_table_style = 'Table Style Medium 3'
        # self.excel_table_style='Table Style Medium 9'
        self._excel_path = excel_path
        # self.excel_path = r"C:\Users\dp26422\PycharmProjects\mortgage\my_mix_statistics.xlsx"
        self.interest_rates_joint_index = self.init_interest_excel_parsers(interest_rates_joint_index_excel)
        self.interest_rates_not_joint_index = self.init_interest_excel_parsers(interest_rates_not_joint_index_excel)
        self.interest_rates_prognosis_joint_index_excel = self.init_interest_prognosis_excel_parsers(interest_rates_prognosis_joint_index_excel)
        self.interest_rates_prognosis_not_joint_index_excel = self.init_interest_prognosis_excel_parsers(interest_rates_prognosis_not_joint_index_excel)

        # print(self)

    @property
    def excel_path(self):
        return self._excel_path

    @excel_path.setter
    def excel_path(self, dirname):
        if os.path.isdir(dirname):
            self._excel_path = os.path.join(dirname, self.name + '.xlsx')

    def init_interest_excel_parsers(self, x):
        if isinstance(x, InterestExcelParser):
            return x
        else:
            return InterestExcelParser(x)

    def init_interest_prognosis_excel_parsers(self, x):
        if isinstance(x, InterestPrognosisExcelParser):
            return x
        else:
            return InterestPrognosisExcelParser(x)


    @property
    def mix_inital_amount(self):
        return sum([t.initial_amount for t in self.tracks])

    @property
    def mix_monthly_return(self):
        mix_monthly_return_array = np.zeros(self.longest_track)
        for track in self.tracks:
            mix_monthly_return_array += self.pad(np.array(track.get_monthly_return_list()))
        return mix_monthly_return_array.tolist()

    @property
    def mix_principal_coverage(self):
        mix_principal_coverage_array = np.zeros(self.longest_track)
        for track in self.tracks:
            mix_principal_coverage_array += self.pad(np.array(track.get_principal_coverage_list()))
        return mix_principal_coverage_array.tolist()

    @property
    def mix_interest_payments(self):
        mix_interest_payments_array = np.zeros(self.longest_track)
        for track in self.tracks:
            mix_interest_payments_array += self.pad(np.array(track.get_interest_payments_list()))
        return mix_interest_payments_array.tolist()

    @property
    def mix_index_payments(self):
        mix_index_payments_array = np.zeros(self.longest_track)
        for track in self.tracks:
            mix_index_payments_array += self.pad(np.array(track.get_index_payments_list()))
        return mix_index_payments_array.tolist()

    @property
    def mix_current_amount(self):
        mix_current_principal_array = np.zeros(self.longest_track)
        for track in self.tracks:
            mix_current_principal_array += self.pad(np.array(track.get_current_principal_list()))
        return mix_current_principal_array.tolist()


    @property
    def mix_total_interest_payed(self):
        return sum(self.mix_interest_payments)

    @property
    def mix_total_index_payments(self):
        return sum(self.mix_index_payments)

    @property
    def mix_total_monthly_return(self):
        return sum(self.mix_monthly_return)

    @property
    def longest_track(self):
        return max([len(i) for i in self.tracks])

    def pad(self, array_to_pad):
        padding_length = self.longest_track - len(array_to_pad)
        return np.pad(array_to_pad, (0, padding_length), 'constant')

    @property
    def return_rate(self):
        mix_loan = sum([track.initial_amount for track in self.tracks])
        return np.round(self.mix_total_monthly_return / mix_loan, 6)

    @property
    def mix_average_monthly_return(self):
        return np.round(sum(self.mix_monthly_return) / self.longest_track, 1)

    @property
    def mix_max_monthly_return(self):
        return np.round(max(self.mix_monthly_return), 1)

    def write_mix_to_sheet(self):

        workbook = xlsxwriter.Workbook(self.excel_path)
        entry_format = workbook.add_format()
        entry_format.set_text_wrap()  # Allow new-lines inside cells
        entry_format.set_align('right')
        entry_format.set_align('vupper')

        column_header_format = workbook.add_format()
        column_header_format.set_align('left')
        column_header_format.set_bold()
        for track in self.tracks:
            worksheet = workbook.add_worksheet(track.name)
            column_names = ["       חודש", "       תשלום ריבית", "       תשלום הצמדה", "       סגירת קרן", "       החזר חודשי", "       יתרת הקרן"]
            track_table = list(zip(range(0, len(self)),
                                   track.get_interest_payments_list(),
                                   track.get_index_payments_list(),
                                   track.get_principal_coverage_list(),
                                   track.get_monthly_return_list(),
                                   track.get_current_principal_list()
                                   )
                               )
            # Write column headers with bold
            for i, column in enumerate(column_names):
                worksheet.write(0, i, column, column_header_format)

            # Create a table to the worksheet.
            columns_for_table = [{'header': col_name} for col_name in column_names]
            worksheet.add_table('A1:{}{}'.format(chr(ord('A') + len(column_names) - 1), len(track_table) + 1), {'data': track_table,
                                                                                                                'columns': columns_for_table,
                                                                                                                'style': self.excel_table_style
                                                                                                                }
                                )

        worksheet = workbook.add_worksheet(self.name)
        for i, column in enumerate(column_names):
            worksheet.write(0, i, column, column_header_format)

        # Create a table to the worksheet.
        mix_table = list(zip(range(0, len(self)),
                             self.mix_interest_payments,
                             self.mix_index_payments,
                             self.mix_principal_coverage,
                             self.mix_monthly_return,
                             self.mix_current_amount
                             )
                         )
        columns_for_table = [{'header': col_name} for col_name in column_names]
        worksheet.add_table('A1:{}{}'.format(chr(ord('A') + len(column_names) - 1), len(mix_table) + 1), {'data': mix_table,
                                                                                                          'columns': columns_for_table,
                                                                                                          'style': self.excel_table_style
                                                                                                          }
                            )
        # Configure the first series.
        chart1 = workbook.add_chart({'type': 'line'})

        chart1.add_series({
            'name': "החזר חודשי",
            'categories': '={}!$A$2:$A${}'.format(self.name, self.longest_track + 1),
            'values': '={}!$E$2:$E${}'.format(self.name, self.longest_track + 1),
        })

        # Add a chart title and some axis labels.
        chart1.set_title({'name': 'החזר חודשי'})
        chart1.set_x_axis({'name': 'חודש'})
        chart1.set_y_axis({'name': 'החזר בשקלים', 'min': int(min(self.mix_monthly_return)/1.05), 'max': int(max(self.mix_monthly_return)*1.05)})
        # Set an Excel chart style. Colors with white outline and shadow.
        chart1.set_style(10)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart('J4', chart1, {'x_scale': 1.5, 'Y_scale': 4})

        years = np.arange(self.longest_track/12).tolist()
        interest_per_year = np.sum(np.split(np.array(self.mix_interest_payments), len(years)), axis=1).tolist()
        principal_coverage_per_year = np.sum(np.split(np.array(self.mix_principal_coverage), len(years)), axis=1).tolist()

        intermidiate_calcs_offset = 1000
        headings = "year interest principal".split()
        worksheet.write_row('A{}'.format(intermidiate_calcs_offset), headings)
        worksheet.write_column('A{}'.format(intermidiate_calcs_offset+1), years)
        worksheet.write_column('B{}'.format(intermidiate_calcs_offset+1), interest_per_year)
        worksheet.write_column('C{}'.format(intermidiate_calcs_offset+1), principal_coverage_per_year)


        chart2 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
        # chart2 = workbook.add_chart({'type': 'area', 'subtype': 'percent_stacked'})
        chart2.add_series({
            'name': "החזר קרן",
            'categories': '={}!$A${}:$A${}'.format(self.name, intermidiate_calcs_offset+1, intermidiate_calcs_offset+1 + len(years)),
            'values': '={}!$C${}:$C${}'.format(self.name, intermidiate_calcs_offset+1, intermidiate_calcs_offset+1 + len(years))
        })

        chart2.add_series({
            'name': "החזר ריבית",
            'categories': '={}!$A${}:$A${}'.format(self.name, intermidiate_calcs_offset+1, intermidiate_calcs_offset+1 + len(years)),
            'values': '={}!$B${}:$B${}'.format(self.name, intermidiate_calcs_offset+1, intermidiate_calcs_offset+1 + len(years))
        })

        # Add a chart title and some axis labels.
        chart2.set_title({'name': 'יחס בין סגירת קרן לתשלום ריבית'})
        chart2.set_x_axis({'name': 'שנה'})
        chart2.set_y_axis({'name': 'החזר כולל'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart2.set_style(11)
        # Insert the chart into the worksheet (with an offset).
        worksheet.insert_chart('J21', chart2, {'x_scale': 1.5, 'Y_scale': 4})

        workbook.close()

    def calc_market_space(self):
        # TODO(Natan): this is according to NPV youtube video. in order to deriviate constant interest from changing values
        # const_to_changing_interest_ration = 0.5
        years = 5   # The interest is changing every 5 years
        min_statistics_year = 2018 # TODO(Natan): Simply by looking at the data. Could be changed!

        market_spacing = 0
        diff = 0
        # TODO(Natan): Need to figure out how eligibility loan affects market space. currently its ignored
        total_loan_amount = 0
        for track in self.tracks:
            # if "eligibility" not in track.name.lower():
            total_loan_amount += track.initial_amount

        for track in self.tracks:
            if "prime" in track.name.lower():
                diff = track.initial_interest - track.bank_predicted_anchor[0]

            elif "changing" in track.name.lower():
                if "not joint" in track.name.lower():
                    diff = track.initial_interest - self.interest_rates_prognosis_not_joint_index_excel.get_latest_prognosis(years, min_statistics_year)/12/100
                    # diff = track.initial_interest - self.interest_rates_prognosis_not_joint_index_excel.get_prognosis_diff(years, min_statistics_year, method='mean')/12/100
                else:
                    diff = track.initial_interest - self.interest_rates_prognosis_joint_index_excel.get_latest_prognosis(years, min_statistics_year)/12/100
                    # diff = track.initial_interest - self.interest_rates_prognosis_joint_index_excel.get_prognosis_diff(years, min_statistics_year, method='mean')/12/100

            elif "constant" in track.name.lower():
                if track.name.lower() in ["joint", "eligibility"]:
                    diff = track.initial_interest - self.interest_rates_prognosis_joint_index_excel.get_prognosis(track.get_mean_life_span()/12)/12/100
                else:
                    diff = track.initial_interest - self.interest_rates_prognosis_not_joint_index_excel.get_prognosis(track.get_mean_life_span()/12)/12/100

            track_weight = track.initial_amount / total_loan_amount
            market_spacing += track_weight * diff * 12 * 100
            # print("track {} diff is {} weight is {}".format(track.name.lower(), diff * 12 * 100, track_weight))
        return market_spacing

    def __len__(self):
        return self.longest_track

    def __str__(self):
        header = "פירוט מסלולים \n".format(self.name)
        printed_str = header + "=" * len(header) + "\n"
        for track in self.tracks:
            printed_str += str(track)

        header = "סיכום תמהיל: {} \n".format(self.name)
        printed_str += header + "=" * len(header) + "\n"

        printed_str += "סך הלוואה: {}\n" \
                      "החזר חודשי מינימאלי: {}\n" \
                      "החזר חודשי מקסימלי: {}\n" \
                      "החזר ריבית: {}\n" \
                      "החזר הצמדת מדד: {}\n" \
                      "החזר בסוף תקופה: {}\n" \
                      "יחס החזר: {}\n" \
                      "מרווח שוק: {}\n" \
                       "\n"

        return printed_str.format(
                           int(self.mix_inital_amount),
                           int(min(self.mix_monthly_return)),
                           int(max(self.mix_monthly_return)),
                           int(self.mix_total_interest_payed),
                           int(self.mix_total_index_payments),
                           int(self.mix_total_monthly_return),
                           np.round(self.return_rate, 2),
                           np.round(self.calc_market_space(), 2)
                           )


if __name__ == '__main__':

    yearly_interest_percent = 1.6
    yearly_index_percent = 0.6
    loan_amount = 1.05e6 * 0.3
    loan_years = 20

    loan_months = 12 * loan_years
    t1 = Track(months=loan_months,
               amount=loan_amount,
               interest=yearly_interest_percent,
               index=yearly_index_percent,
               name="constant joint",
               interest_model='const',
               index_model='finwiz_index'
               )

    yearly_interest_percent = 1
    yearly_index_percent = 0
    loan_amount = 1.05e6/3
    loan_years = 20

    loan_months = 12 * loan_years
    t2 = Track(months=loan_months,
               amount=loan_amount,
               interest=yearly_interest_percent,
               index=yearly_index_percent,
               name="prime",
               interest_model='finwiz_prime',
               index_model=''
               )

    yearly_interest_percent = 2.2
    yearly_index_percent = 0.6
    loan_amount = 1.05e6 - 1.05e6/3 - 1.05e6 * 0.3
    loan_years = 20

    loan_months = 12 * loan_years
    t3 = Track(months=loan_months,
               amount=loan_amount,
               interest=yearly_interest_percent,
               index=yearly_index_percent,
               name="changing joint",
               interest_model='finwiz_changing_w_index',
               index_model='finwiz_index',
               early_closure=(10*12, -1)
               )

    yearly_interest_percent = 1.6
    loan_amount = 86000
    loan_years = 10

    loan_months = 12 * loan_years
    t4 = Track(months=loan_months,
               amount=loan_amount,
               interest=yearly_interest_percent,
               name="eligibility",
               interest_model='const',
               index_model='finwiz_index'
               )


    excel_path = r"C:\Users\dp26422\Desktop\my_mix_statistics.xlsx"
    first_mix = Mix([t3],
    # first_mix = Mix([t1, t2, t3, t4],
                    "התמהיל_הראשון_שלי!",
                    excel_path,
                    interest_rates_joint_index_excel=os.path.abspath("interests/joint.xlsx"),
                    interest_rates_not_joint_index_excel=os.path.abspath("interests/not_joint.xlsx"),
                    interest_rates_prognosis_joint_index_excel=os.path.abspath("interests/joint_interest_prognosis_processed.xls"),
                    interest_rates_prognosis_not_joint_index_excel=os.path.abspath("interests/not_joint_interest_prognosis_processed.xls"),

                    )
    print(first_mix)

    # print(first_mix.mix_monthly_return)
    # fig, ax = plt.subplots()
    # ax.plot(range(len(first_mix)), first_mix.mix_monthly_return, '-b', label='Monthly returns')
    # # ax.plot(range(len(first_mix)), first_mix.mix_interest_payments, '-.r', label='Interest returns returns')
    # leg = ax.legend()
    # plt.show

    first_mix.write_mix_to_sheet()
