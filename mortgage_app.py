import json
import os
import wx
import wx.aui as aui

try:
    import agw.flatnotebook as FNB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatnotebook as FNB

import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from ui.oc.gui import Mainframe
from track import Track
from mix import Mix
from interest_excel_parser import InterestExcelParser
from interest_prognosis_excel_parser import InterestPrognosisExcelParser



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass


# class CanvasPanel(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         self.figure = Figure()
#         self.axes1 = self.figure.add_subplot(211)
#         self.axes2 = self.figure.add_subplot(212)
#         self.canvas = FigureCanvas(self, -1, self.figure)
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
#         self.SetSizer(self.sizer)
#         self.Fit()
#
#     def draw_monthly_return(self, monthly_returns, months):
#         self.axes1.plot(months, monthly_returns)
#
#     def draw_interest_vs_principal(self, interest, principal, years):
#         self.axes2.bar(years, interest)
#         self.axes2.bar(years, principal)
#
#     def draw(self):
#         t = np.arange(0.0, 3.0, 0.01)
#         s = np.sin(2 * np.pi * t)
#         c = np.cos(2 * np.pi * t)
#         self.axes1.plot(t, s)
#         self.axes2.plot(t, c)

class MortgageApp(Mainframe):
    def __init__(self, parent):
        super().__init__(parent)

        self.mix = None
        self.number_of_tracks = 4
        self.app_state_dict = {}
        self.max_interest_for_scroller = 5.
        self.interest_scroll_step_size = self.max_interest_for_scroller / (self.m_slider_interest_track1.GetMax() - self.m_slider_interest_track1.GetMin())

        self.interest_rates_joint_index = InterestExcelParser(os.path.abspath("interests/joint.xlsx"))
        self.interest_rates_not_joint_index = InterestExcelParser(os.path.abspath("interests/not_joint.xlsx"))
        self.interest_rates_eligibility = InterestExcelParser(os.path.abspath("interests/eligibility.xlsx"))

        self.interest_rates_prognosis_joint_index_excel = InterestPrognosisExcelParser("interests/joint_interest_prognosis_processed.xls")
        self.interest_rates_prognosis_not_joint_index_excel = InterestPrognosisExcelParser("interests/not_joint_interest_prognosis_processed.xls")

        self.done_loading = True

        # Init methods

        self.plotting_panel_init()
        self.init_notebook()

    def init_notebook(self):
        bookStyle = aui.AUI_NB_DEFAULT_STYLE
        bookStyle &= ~(aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
        self.nb = aui.AuiNotebook(self, style=bookStyle)

        bookStyle = FNB.FNB_NODRAG
        # self.nb = FNB.FlatNotebook(self, wx.ID_ANY, agwStyle=bookStyle)

        self.nb.AddPage(self.m_mainPanel, "Mix tab")
        #
        # for num in range(1, 5):
        #     page = wx.TextCtrl(self.nb, -1, "This is page %d" % num ,
        #                        style=wx.TE_MULTILINE)
        #     self.nb.AddPage(page, "Tab Number %d" % num)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.nb.SendSizeEvent)


    # Plotting panel initialization
    def plotting_panel_init(self):
        self.m_ploting_canvas_panel.figure = Figure()
        self.m_ploting_canvas_panel.axes1 = self.m_ploting_canvas_panel.figure.add_subplot(211)
        self.m_ploting_canvas_panel.axes2 = self.m_ploting_canvas_panel.figure.add_subplot(212)
        self.m_ploting_canvas_panel.canvas = FigureCanvas(self.m_ploting_canvas_panel, -1, self.m_ploting_canvas_panel.figure)
        self.m_ploting_canvas_panel.sizer = wx.BoxSizer(wx.VERTICAL)
        self.m_ploting_canvas_panel.sizer.Add(self.m_ploting_canvas_panel.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.m_ploting_canvas_panel.SetSizer(self.m_ploting_canvas_panel.sizer)
        self.m_ploting_canvas_panel.Fit()


    # Events handling
    def m_CalculateStatsOnButtonClick(self, event):
        self.create_and_display_mix()
        self.create_and_display_mix()

    def m_choice_track1OnChoice(self, event):
        self.display_interest(track_number=1)
        # self.create_and_display_mix()

    def m_choice_track2OnChoice(self, event):
        self.display_interest(track_number=2)
        # self.create_and_display_mix()

    def m_choice_track3OnChoice(self, event):
        self.display_interest(track_number=3)
        # self.create_and_display_mix()

    def m_choice_track4OnChoice(self, event):
        self.display_interest(track_number=4)
        # self.create_and_display_mix()

    def m_textCtrl_Track1_MonthsOnText(self, event):
        self.display_interest(track_number=1)
        # self.create_and_display_mix()

    def m_textCtrl_Track2_MonthsOnText(self, event):
        self.display_interest(track_number=2)
        # self.create_and_display_mix()

    def m_textCtrl_Track3_MonthsOnText(self, event):
        self.display_interest(track_number=3)
        # self.create_and_display_mix()

    def m_textCtrl_Track4_MonthsOnText(self, event):
        self.display_interest(track_number=4)
        # self.create_and_display_mix()

    def textCtrl_funding_percentageOnText(self, event):
        percentage = self.textCtrl_funding_percentage.GetValue()
        if percentage:
            percentage = int(percentage)
            if 75 > percentage > 45:
                for track_num in range(1, self.number_of_tracks+1):
                    self.display_interest(track_num)
            else:
                return

    def m_create_excel_reportOnButtonClick(self, event):
        path = self.m_dirPicker_for_excel_output.GetPath()
        if path:
            self.mix.excel_path = path
            self.mix.write_mix_to_sheet()

    def m_menuItem_new_mixOnMenuSelection(self, event):
        default_val = {"m_choice_track": "--Choose type--",
                       "m_early_closure_choise_track": "No"
                       }
        for obj in vars(self):
            wx_object = getattr(self, obj)
            if isinstance(wx_object, wx.Choice):
                for choise_type, val in default_val.items():
                    if choise_type in obj:
                        wx_object.SetSelection(wx_object.FindString(val))
            elif isinstance(wx_object, wx.TextCtrl):
                wx_object.Clear()
            else:
                pass
        self.m_ploting_canvas_panel.canvas.ClearBackground()

    def m_menuItem_save_mixOnMenuSelection(self, event):
        try:
            dlg = wx.FileDialog(self, "Save to file:", ".", "", "JSON (*.json)|*.json", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                json_save_file_path = os.path.join(self.dirname, self.filename)
                with open(json_save_file_path, 'w') as f:
                    json.dump(self.app_state_dict, f)
            dlg.Destroy()
        except:
            pass

    def m_menuItem_load_mixOnMenuSelection(self, event):
        self.done_loading = False
        wildcard = "json files (*.json)|*.json"
        dialog = wx.FileDialog(self, "Open Json Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                loaded_dict = json.load(f)
                for control, val in loaded_dict.items():
                    wx_object = getattr(self, control)
                    if isinstance(wx_object, wx.Choice):
                        wx_object.SetSelection(wx_object.FindString(val))
                    elif isinstance(wx_object, wx.TextCtrl):
                        wx_object.SetValue(str(val))
                    else:
                        pass
        self.done_loading = True
        self.create_and_display_mix()


    def m_slider_interest_track1OnScrollChanged(self, event):
        scroller_value = int(self.m_slider_interest_track1.GetValue())
        self.m_textCtrl_Track1_Interest.SetValue(str(np.round(scroller_value*self.interest_scroll_step_size, 2)))
        self.create_and_display_mix()

    def m_slider_interest_track2OnScrollChanged(self, event):
        scroller_value = int(self.m_slider_interest_track2.GetValue())
        self.m_textCtrl_Track2_Interest.SetValue(str(np.round(scroller_value*self.interest_scroll_step_size, 2)))
        self.create_and_display_mix()


    def m_slider_interest_track3OnScrollChanged(self, event):
        scroller_value = int(self.m_slider_interest_track3.GetValue())
        self.m_textCtrl_Track3_Interest.SetValue(str(np.round(scroller_value*self.interest_scroll_step_size, 2)))
        self.create_and_display_mix()

    def m_slider_interest_track4OnScrollChanged(self, event):
        scroller_value = int(self.m_slider_interest_track4.GetValue())
        self.m_textCtrl_Track4_Interest.SetValue(str(np.round(scroller_value*self.interest_scroll_step_size, 2)))
        self.create_and_display_mix()


    # Additional methods
    def create_and_display_mix(self):
        self.create_mix()
        print(self.mix)
        if self.mix.tracks:
            self.display_mix_stats()
        self.draw_plots()
        return

    def create_mix(self):
        fields_names = "Amount Interest Months".split()
        # fields_names = "Name Amount Interest Index Months".split()
        tracks = []
        for track_num in range(1, self.number_of_tracks+1):
            track_dict = {}
            skip_track = False
            for fields_name in fields_names:
                control_name = "m_textCtrl_Track{}_{}".format(track_num, fields_name)
                val = getattr(self, control_name).GetValue()
                self.app_state_dict[control_name] = val
                if val:
                    track_dict[fields_name.lower()] = val if not is_number(eval(val)) else float(eval(val))
                else:
                    skip_track = True
                    break
            if not skip_track:  # .SetSelection()
                interest_yearly_addition_every_five = 1
                control_name = 'm_choice_track{}'.format(track_num)
                track_type = getattr(self, control_name).GetStringSelection()
                self.app_state_dict[control_name] = track_type

                control_name = 'm_early_closure_choise_track{}'.format(track_num)
                early_close = getattr(self, control_name.format(track_num)).GetStringSelection()
                self.app_state_dict[control_name] = early_close
                if early_close == 'Yes':
                    control_name = 'textCtrl_closure_month_track{}'.format(track_num)
                    closure_month = getattr(self, control_name).GetValue()
                    self.app_state_dict[control_name] = closure_month
                    closure_month = int(eval(closure_month))
                    track_dict.update({"early_closure": (closure_month, -1)})   # TODO(Natan): Need to allow specific amount closure

                interest_modeling = 'const'  # Default
                if "constant" in track_type.lower() or "eligibility" in track_type.lower():
                    interest_modeling = 'const'
                elif "prime" in track_type.lower():
                    interest_modeling = 'npv_prime'
                    # interest_modeling = 'finwiz_prime'
                    # interest_modeling = 'model'
                else:
                    # interest_modeling = 'changing'
                    if "joint" in track_type.lower():
                        interest_modeling = "finwiz_changing_w_index"
                        # interest_yearly_addition_every_five = self.interest_rates_prognosis_joint_index_excel.get_prognosis_diff(years=5,
                        #                                                                                                          min_statistics_year=2018,
                                                                                                                                 # method='mean')
                    if "not joint" in track_type.lower():
                        interest_modeling = "finwiz_changing_wo_index"
                        # interest_yearly_addition_every_five = self.interest_rates_prognosis_not_joint_index_excel.get_prognosis_diff(years=5,
                        #                                                                                                              min_statistics_year=2018,
                                                                                                                                     # method='mean')

                if track_type.lower() in ["constant joint", "changing joint", "eligibility"]:
                    index_modeling = 'npv_index'
                    # index_modeling = 'finwiz_index'
                else:
                    index_modeling = 'const'

                track_dict.update({'interest_model': interest_modeling,
                                   'index_model': index_modeling,
                                   'name': track_type,
                                   # 'interest_yearly_addition_every_five': interest_yearly_addition_every_five
                                   })
                track = Track(**track_dict)
                tracks.append(track)

        self.app_state_dict['textCtrl_mix_name'] = self.textCtrl_mix_name.GetValue()
        self.mix = Mix(tracks,
                       name=self.textCtrl_mix_name.GetValue(),
                       interest_rates_joint_index_excel=self.interest_rates_joint_index,
                       interest_rates_not_joint_index_excel=self.interest_rates_joint_index,
                       interest_rates_prognosis_joint_index_excel=self.interest_rates_prognosis_joint_index_excel,
                       interest_rates_prognosis_not_joint_index_excel=self.interest_rates_prognosis_not_joint_index_excel

                       )

    def display_interest(self, track_number):
        months = getattr(self, "m_textCtrl_Track{}_{}".format(track_number, 'Months')).GetValue()
        try:
            eval(months)
        except:
            return

        # mortgage is for at least years
        if int(eval(months)) < (4 * 12):
            return
        track_type_choise = getattr(self, 'm_choice_track{}'.format(track_number)).GetStringSelection()

        if months and '--Choose type--' != track_type_choise:
            funding_percentage = int(self.textCtrl_funding_percentage.GetValue())
            self.app_state_dict['textCtrl_funding_percentage'] = funding_percentage
            track_duration = int(eval(months)) / 12
            if track_type_choise.lower() in "eligibility":
                interest = self.interest_rates_eligibility.query_percentage(funding_percentage, track_duration)
            elif track_type_choise.lower() in ["constant joint", "changing joint"]:
                track_duration_or_track_name = track_duration if "constant" in track_type_choise.lower() else "changing"
                interest = self.interest_rates_joint_index.query_percentage(funding_percentage, track_duration_or_track_name)
            else:
                track_type = track_type_choise.lower().split()[0]
                track_duration_or_track_name = track_duration if "constant" in track_type else track_type
                interest = self.interest_rates_not_joint_index.query_percentage(funding_percentage, track_duration_or_track_name)
            # print(interest)
            if self.done_loading:
                getattr(self, "m_textCtrl_Track{}_{}".format(track_number, 'Interest')).SetValue(str(np.round(interest, 2)))
                getattr(self, "m_slider_interest_track{}".format(track_number,)).SetValue(int(interest/self.interest_scroll_step_size))


            control_name = "m_textCtrl_Track{}_{}".format(track_number, 'Interest')
            self.app_state_dict[control_name] = str(np.round(interest, 2))
        return

    def display_mix_stats(self):
        self.m_textCtrl_first_return.SetValue(str(int(self.mix.mix_monthly_return[0])) + u"\u20AA")
        self.m_textCtrl_average_return.SetValue(str(int(self.mix.mix_average_monthly_return)) + u"\u20AA")
        self.m_textCtrl_maximum_return.SetValue(str(int(self.mix.mix_max_monthly_return)) + u"\u20AA")
        self.m_textCtrl_return_ratio.SetValue(str(np.round(self.mix.return_rate, 2)))
        self.m_textCtrl_total_interest_return.SetValue(str(int(self.mix.mix_total_interest_payed)) + u"\u20AA")
        self.m_textCtrl_total_index_return.SetValue(str(int(self.mix.mix_total_index_payments)) + u"\u20AA")
        self.m_textCtrl_total_return.SetValue(str(int(self.mix.mix_total_monthly_return)) + u"\u20AA")
        self.m_textCtrl_market_space.SetValue(str(np.round(self.mix.calc_market_space(), 2)))
        return

    def draw_plots(self):
        self.m_ploting_canvas_panel.Fit()
        self.m_ploting_canvas_panel.axes1.clear()
        self.m_ploting_canvas_panel.axes2.clear()
        avg_yearly_monthly_return = np.mean(np.split(np.array(self.mix.mix_monthly_return), self.mix.longest_track//12), axis=1)
        self.m_ploting_canvas_panel.axes1.set_xticks(range(len(avg_yearly_monthly_return)))
        self.m_ploting_canvas_panel.axes1.set_ylabel('Average Monthly Return')
        self.m_ploting_canvas_panel.axes1.set_xlabel('Year')
        self.m_ploting_canvas_panel.axes1.plot(range(len(avg_yearly_monthly_return)), avg_yearly_monthly_return)

        years = np.arange(self.mix.longest_track/12).tolist()
        interest_per_year = np.sum(np.split(np.array(self.mix.mix_interest_payments), len(years)), axis=1).tolist()
        principal_coverage_per_year = np.sum(np.split(np.array(self.mix.mix_principal_coverage), len(years)), axis=1).tolist()

        self.m_ploting_canvas_panel.axes2.bar(years, principal_coverage_per_year, color='#7FC9FF')
        self.m_ploting_canvas_panel.axes2.bar(years, interest_per_year, bottom=principal_coverage_per_year, color='#7FFFFF')
        self.m_ploting_canvas_panel.axes2.tick_params()

        self.m_ploting_canvas_panel.axes2.set_ylabel('Yearly return')
        self.m_ploting_canvas_panel.axes2.set_xlabel('Years')
        self.m_ploting_canvas_panel.axes2.set_xticks(years)
        self.m_ploting_canvas_panel.axes2.legend(('Principal return', 'Interest return'))

        self.m_ploting_canvas_panel.figure.tight_layout(pad=1.)
        self.m_ploting_canvas_panel.canvas.draw()

class MainApp(wx.App):
    def OnInit(self):
        mainFrame = MortgageApp(None)
        mainFrame.Show(True)
        return True


if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
