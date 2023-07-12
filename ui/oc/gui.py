# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Mainframe
###########################################################################

class Mainframe ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"מחשבון משכנתא", pos = wx.DefaultPosition, size = wx.Size( 900,811 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_mainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,400 ), wx.TAB_TRAVERSAL )
		bSizerMainPanel = wx.BoxSizer( wx.VERTICAL )

		bSizerPanelMain = wx.BoxSizer( wx.VERTICAL )

		bSizer_mix_name = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer163 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Mix Name" ), wx.VERTICAL )

		self.textCtrl_mix_name = wx.TextCtrl( sbSizer163.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer163.Add( self.textCtrl_mix_name, 0, wx.ALL, 5 )


		bSizer_mix_name.Add( sbSizer163, 1, wx.EXPAND, 5 )

		sbSizer1631 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Funding percentage" ), wx.VERTICAL )

		self.textCtrl_funding_percentage = wx.TextCtrl( sbSizer1631.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1631.Add( self.textCtrl_funding_percentage, 0, wx.ALL, 5 )


		bSizer_mix_name.Add( sbSizer1631, 1, wx.EXPAND, 0 )


		bSizerPanelMain.Add( bSizer_mix_name, 0, wx.EXPAND, 5 )

		bSizerTrack1 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer173 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Track type" ), wx.VERTICAL )

		m_choice_track1Choices = [ u"--Choose type--", u"Prime", u"Constant Joint", u"Constant Not Joint", u"Changing Joint", u"Changing Not Joint", u"Eligibility", u"Eligibility", wx.EmptyString ]
		self.m_choice_track1 = wx.Choice( sbSizer173.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_track1Choices, 0 )
		self.m_choice_track1.SetSelection( 0 )
		sbSizer173.Add( self.m_choice_track1, 0, wx.ALL, 5 )


		bSizerTrack1.Add( sbSizer173, 1, wx.EXPAND, 5 )

		sbSizer13 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Amount" ), wx.VERTICAL )

		self.m_textCtrl_Track1_Amount = wx.TextCtrl( sbSizer13.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer13.Add( self.m_textCtrl_Track1_Amount, 0, wx.ALL, 5 )


		bSizerTrack1.Add( sbSizer13, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )

		sbSizer17 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Months" ), wx.VERTICAL )

		self.m_textCtrl_Track1_Months = wx.TextCtrl( sbSizer17.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer17.Add( self.m_textCtrl_Track1_Months, 0, wx.ALL, 5 )


		bSizerTrack1.Add( sbSizer17, 1, wx.EXPAND, 5 )

		sbSizer15 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Interest" ), wx.VERTICAL )

		self.m_textCtrl_Track1_Interest = wx.TextCtrl( sbSizer15.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer15.Add( self.m_textCtrl_Track1_Interest, 0, wx.ALL, 5 )

		self.m_slider_interest_track1 = wx.Slider( sbSizer15.GetStaticBox(), wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		sbSizer15.Add( self.m_slider_interest_track1, 0, wx.ALL, 5 )


		bSizerTrack1.Add( sbSizer15, 1, wx.EXPAND, 5 )

		sbSizer1733 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Early closure   Closure month" ), wx.HORIZONTAL )

		m_early_closure_choise_track1Choices = [ u"No", u"Yes" ]
		self.m_early_closure_choise_track1 = wx.Choice( sbSizer1733.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_early_closure_choise_track1Choices, 0 )
		self.m_early_closure_choise_track1.SetSelection( 0 )
		sbSizer1733.Add( self.m_early_closure_choise_track1, 0, wx.ALL, 5 )

		self.textCtrl_closure_month_track1 = wx.TextCtrl( sbSizer1733.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1733.Add( self.textCtrl_closure_month_track1, 0, wx.ALL, 5 )


		bSizerTrack1.Add( sbSizer1733, 1, wx.EXPAND, 5 )


		bSizerPanelMain.Add( bSizerTrack1, 0, wx.ALIGN_RIGHT|wx.EXPAND, 0 )

		bSizerTrack2 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer1731 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Track type" ), wx.VERTICAL )

		m_choice_track2Choices = [ u"--Choose type--", u"Prime", u"Constant Joint", u"Constant Not Joint", u"Changing Joint", u"Changing Not Joint", u"Eligibility" ]
		self.m_choice_track2 = wx.Choice( sbSizer1731.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_track2Choices, 0 )
		self.m_choice_track2.SetSelection( 0 )
		sbSizer1731.Add( self.m_choice_track2, 0, wx.ALL, 5 )


		bSizerTrack2.Add( sbSizer1731, 1, wx.EXPAND, 5 )

		sbSizer131 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Amount" ), wx.VERTICAL )

		self.m_textCtrl_Track2_Amount = wx.TextCtrl( sbSizer131.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer131.Add( self.m_textCtrl_Track2_Amount, 0, wx.ALL, 5 )


		bSizerTrack2.Add( sbSizer131, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )

		sbSizer171 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Months" ), wx.VERTICAL )

		self.m_textCtrl_Track2_Months = wx.TextCtrl( sbSizer171.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer171.Add( self.m_textCtrl_Track2_Months, 0, wx.ALL, 5 )


		bSizerTrack2.Add( sbSizer171, 1, wx.EXPAND, 5 )

		sbSizer151 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Interest" ), wx.VERTICAL )

		self.m_textCtrl_Track2_Interest = wx.TextCtrl( sbSizer151.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer151.Add( self.m_textCtrl_Track2_Interest, 0, wx.ALL, 5 )

		self.m_slider_interest_track2 = wx.Slider( sbSizer151.GetStaticBox(), wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		sbSizer151.Add( self.m_slider_interest_track2, 0, wx.ALL, 5 )


		bSizerTrack2.Add( sbSizer151, 1, wx.EXPAND, 5 )

		sbSizer17331 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Early closure   Closure month" ), wx.HORIZONTAL )

		m_early_closure_choise_track2Choices = [ u"No", u"Yes" ]
		self.m_early_closure_choise_track2 = wx.Choice( sbSizer17331.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_early_closure_choise_track2Choices, 0 )
		self.m_early_closure_choise_track2.SetSelection( 0 )
		sbSizer17331.Add( self.m_early_closure_choise_track2, 0, wx.ALL, 5 )

		self.textCtrl_closure_month_track2 = wx.TextCtrl( sbSizer17331.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer17331.Add( self.textCtrl_closure_month_track2, 0, wx.ALL, 5 )


		bSizerTrack2.Add( sbSizer17331, 1, wx.EXPAND, 5 )


		bSizerPanelMain.Add( bSizerTrack2, 0, wx.EXPAND, 1 )

		bSizerTrack3 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer1732 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Track type" ), wx.VERTICAL )

		m_choice_track3Choices = [ u"--Choose type--", u"Prime", u"Constant Joint", u"Constant Not Joint", u"Changing Joint", u"Changing Not Joint", u"Eligibility" ]
		self.m_choice_track3 = wx.Choice( sbSizer1732.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_track3Choices, 0 )
		self.m_choice_track3.SetSelection( 0 )
		sbSizer1732.Add( self.m_choice_track3, 0, wx.ALL, 5 )


		bSizerTrack3.Add( sbSizer1732, 1, wx.EXPAND, 5 )

		sbSizer132 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Amount" ), wx.VERTICAL )

		self.m_textCtrl_Track3_Amount = wx.TextCtrl( sbSizer132.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer132.Add( self.m_textCtrl_Track3_Amount, 0, wx.ALL, 5 )


		bSizerTrack3.Add( sbSizer132, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )

		sbSizer172 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Months" ), wx.VERTICAL )

		self.m_textCtrl_Track3_Months = wx.TextCtrl( sbSizer172.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer172.Add( self.m_textCtrl_Track3_Months, 0, wx.ALL, 5 )


		bSizerTrack3.Add( sbSizer172, 1, wx.EXPAND, 5 )

		sbSizer152 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Interest" ), wx.VERTICAL )

		self.m_textCtrl_Track3_Interest = wx.TextCtrl( sbSizer152.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer152.Add( self.m_textCtrl_Track3_Interest, 0, wx.ALL, 5 )

		self.m_slider_interest_track3 = wx.Slider( sbSizer152.GetStaticBox(), wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		sbSizer152.Add( self.m_slider_interest_track3, 0, wx.ALL, 5 )


		bSizerTrack3.Add( sbSizer152, 1, wx.EXPAND, 5 )

		sbSizer17332 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Early closure   Closure month" ), wx.HORIZONTAL )

		m_early_closure_choise_track3Choices = [ u"No", u"Yes" ]
		self.m_early_closure_choise_track3 = wx.Choice( sbSizer17332.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_early_closure_choise_track3Choices, 0 )
		self.m_early_closure_choise_track3.SetSelection( 0 )
		sbSizer17332.Add( self.m_early_closure_choise_track3, 0, wx.ALL, 5 )

		self.textCtrl_closure_month_track3 = wx.TextCtrl( sbSizer17332.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer17332.Add( self.textCtrl_closure_month_track3, 0, wx.ALL, 5 )


		bSizerTrack3.Add( sbSizer17332, 1, wx.EXPAND, 5 )


		bSizerPanelMain.Add( bSizerTrack3, 0, wx.EXPAND, 0 )

		bSizerTrack4 = wx.BoxSizer( wx.HORIZONTAL )

		sbSizer17321 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Track type" ), wx.VERTICAL )

		m_choice_track4Choices = [ u"--Choose type--", u"Prime", u"Constant Joint", u"Constant Not Joint", u"Changing Joint", u"Changing Not Joint", u"Eligibility" ]
		self.m_choice_track4 = wx.Choice( sbSizer17321.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_track4Choices, 0 )
		self.m_choice_track4.SetSelection( 0 )
		sbSizer17321.Add( self.m_choice_track4, 0, wx.ALL, 5 )


		bSizerTrack4.Add( sbSizer17321, 1, wx.EXPAND, 5 )

		sbSizer1321 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Amount" ), wx.VERTICAL )

		self.m_textCtrl_Track4_Amount = wx.TextCtrl( sbSizer1321.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1321.Add( self.m_textCtrl_Track4_Amount, 0, wx.ALL, 5 )


		bSizerTrack4.Add( sbSizer1321, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )

		sbSizer1721 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Months" ), wx.VERTICAL )

		self.m_textCtrl_Track4_Months = wx.TextCtrl( sbSizer1721.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1721.Add( self.m_textCtrl_Track4_Months, 0, wx.ALL, 5 )


		bSizerTrack4.Add( sbSizer1721, 1, wx.EXPAND, 5 )

		sbSizer1521 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Interest" ), wx.VERTICAL )

		self.m_textCtrl_Track4_Interest = wx.TextCtrl( sbSizer1521.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer1521.Add( self.m_textCtrl_Track4_Interest, 0, wx.ALL, 5 )

		self.m_slider_interest_track4 = wx.Slider( sbSizer1521.GetStaticBox(), wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		sbSizer1521.Add( self.m_slider_interest_track4, 0, wx.ALL, 5 )


		bSizerTrack4.Add( sbSizer1521, 1, wx.EXPAND, 5 )

		sbSizer17333 = wx.StaticBoxSizer( wx.StaticBox( self.m_mainPanel, wx.ID_ANY, u"Early closure   Closure month" ), wx.HORIZONTAL )

		m_early_closure_choise_track4Choices = [ u"No", u"Yes" ]
		self.m_early_closure_choise_track4 = wx.Choice( sbSizer17333.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_early_closure_choise_track4Choices, 0 )
		self.m_early_closure_choise_track4.SetSelection( 0 )
		sbSizer17333.Add( self.m_early_closure_choise_track4, 0, wx.ALL, 5 )

		self.textCtrl_closure_month_track4 = wx.TextCtrl( sbSizer17333.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer17333.Add( self.textCtrl_closure_month_track4, 0, wx.ALL, 5 )


		bSizerTrack4.Add( sbSizer17333, 1, wx.EXPAND, 5 )


		bSizerPanelMain.Add( bSizerTrack4, 1, wx.EXPAND, 5 )


		bSizerMainPanel.Add( bSizerPanelMain, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Excel Dir:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer10.Add( self.m_staticText7, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

		self.m_dirPicker_for_excel_output = wx.DirPickerCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer10.Add( self.m_dirPicker_for_excel_output, 0, wx.ALL, 0 )


		bSizer16.Add( bSizer10, 1, wx.EXPAND, 0 )

		self.m_CalculateStats = wx.Button( self.m_mainPanel, wx.ID_ANY, u"Create Mix", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_CalculateStats, 0, wx.ALL, 5 )

		self.m_create_excel_report = wx.Button( self.m_mainPanel, wx.ID_ANY, u"Create Excel report", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_create_excel_report, 0, wx.ALL, 5 )


		bSizer14.Add( bSizer16, 1, wx.EXPAND, 5 )

		fgSizer_for_statistics = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer_for_statistics.SetFlexibleDirection( wx.BOTH )
		fgSizer_for_statistics.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText_first_return = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"First return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_first_return.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText_first_return, 0, wx.ALL, 5 )

		self.m_textCtrl_first_return = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_first_return, 0, wx.ALL, 5 )

		self.m_staticText_average_return1 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Average return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_average_return1.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText_average_return1, 0, wx.ALL, 5 )

		self.m_textCtrl_average_return = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_average_return, 0, wx.ALL, 5 )

		self.m_staticText_maximum_return = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Maximum return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_maximum_return.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText_maximum_return, 0, wx.ALL, 5 )

		self.m_textCtrl_maximum_return = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_maximum_return, 0, wx.ALL, 5 )

		self.m_staticText91 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Total interest return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText91, 0, wx.ALL, 5 )

		self.m_textCtrl_total_interest_return = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_total_interest_return, 0, wx.ALL, 5 )

		self.m_staticText911 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Total index return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText911.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText911, 0, wx.ALL, 5 )

		self.m_textCtrl_total_index_return = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_total_index_return, 0, wx.ALL, 5 )

		self.m_staticText9111 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Total return", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9111.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText9111, 0, wx.ALL, 5 )

		self.m_textCtrl_total_return = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_total_return, 0, wx.ALL, 5 )

		self.m_staticText91111 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Return ratio", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91111.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText91111, 0, wx.ALL, 5 )

		self.m_textCtrl_return_ratio = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_return_ratio, 0, wx.ALL, 5 )

		self.m_staticText14 = wx.StaticText( self.m_mainPanel, wx.ID_ANY, u"Market space", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		fgSizer_for_statistics.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_textCtrl_market_space = wx.TextCtrl( self.m_mainPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_for_statistics.Add( self.m_textCtrl_market_space, 0, wx.ALL, 5 )


		bSizer14.Add( fgSizer_for_statistics, 1, wx.EXPAND, 0 )


		bSizer15.Add( bSizer14, 1, wx.ALIGN_LEFT, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_ploting_canvas_panel = wx.Panel( self.m_mainPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer2.Add( self.m_ploting_canvas_panel, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer15.Add( fgSizer2, 1, wx.ALL|wx.EXPAND, 5 )


		bSizerMainPanel.Add( bSizer15, 1, wx.EXPAND, 5 )


		self.m_mainPanel.SetSizer( bSizerMainPanel )
		self.m_mainPanel.Layout()
		bSizer2.Add( self.m_mainPanel, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer2, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu_file = wx.Menu()
		self.m_menuItem_new_mix = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"New mix"+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_new_mix )

		self.m_menuItem_save_mix = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Save mix"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_save_mix )

		self.m_menuItem_load_mix = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Load mix"+ u"\t" + u"Ctrl+L", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_file.Append( self.m_menuItem_load_mix )

		self.m_menubar1.Append( self.m_menu_file, u"File" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.textCtrl_funding_percentage.Bind( wx.EVT_TEXT, self.textCtrl_funding_percentageOnText )
		self.m_choice_track1.Bind( wx.EVT_CHOICE, self.m_choice_track1OnChoice )
		self.m_textCtrl_Track1_Amount.Bind( wx.EVT_TEXT, self.m_textCtrl_Track1_AmountOnText )
		self.m_textCtrl_Track1_Months.Bind( wx.EVT_TEXT, self.m_textCtrl_Track1_MonthsOnText )
		self.m_slider_interest_track1.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_interest_track1OnScrollChanged )
		self.m_early_closure_choise_track1.Bind( wx.EVT_CHOICE, self.m_choice_track1OnChoice )
		self.m_choice_track2.Bind( wx.EVT_CHOICE, self.m_choice_track2OnChoice )
		self.m_textCtrl_Track2_Amount.Bind( wx.EVT_TEXT, self.m_textCtrl_Track2_AmountOnText )
		self.m_textCtrl_Track2_Months.Bind( wx.EVT_TEXT, self.m_textCtrl_Track2_MonthsOnText )
		self.m_slider_interest_track2.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_interest_track2OnScrollChanged )
		self.m_early_closure_choise_track2.Bind( wx.EVT_CHOICE, self.m_choice_track1OnChoice )
		self.m_choice_track3.Bind( wx.EVT_CHOICE, self.m_choice_track3OnChoice )
		self.m_textCtrl_Track3_Amount.Bind( wx.EVT_TEXT, self.m_textCtrl_Track3_AmountOnText )
		self.m_textCtrl_Track3_Months.Bind( wx.EVT_TEXT, self.m_textCtrl_Track3_MonthsOnText )
		self.m_slider_interest_track3.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_interest_track3OnScrollChanged )
		self.m_early_closure_choise_track3.Bind( wx.EVT_CHOICE, self.m_choice_track1OnChoice )
		self.m_choice_track4.Bind( wx.EVT_CHOICE, self.m_choice_track4OnChoice )
		self.m_textCtrl_Track4_Amount.Bind( wx.EVT_TEXT, self.m_textCtrl_Track4_AmountOnText )
		self.m_textCtrl_Track4_Months.Bind( wx.EVT_TEXT, self.m_textCtrl_Track4_MonthsOnText )
		self.m_slider_interest_track4.Bind( wx.EVT_SCROLL_CHANGED, self.m_slider_interest_track4OnScrollChanged )
		self.m_early_closure_choise_track4.Bind( wx.EVT_CHOICE, self.m_choice_track1OnChoice )
		self.m_CalculateStats.Bind( wx.EVT_BUTTON, self.m_CalculateStatsOnButtonClick )
		self.m_create_excel_report.Bind( wx.EVT_BUTTON, self.m_create_excel_reportOnButtonClick )
		self.Bind( wx.EVT_MENU, self.m_menuItem_new_mixOnMenuSelection, id = self.m_menuItem_new_mix.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItem_save_mixOnMenuSelection, id = self.m_menuItem_save_mix.GetId() )
		self.Bind( wx.EVT_MENU, self.m_menuItem_load_mixOnMenuSelection, id = self.m_menuItem_load_mix.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def textCtrl_funding_percentageOnText( self, event ):
		event.Skip()

	def m_choice_track1OnChoice( self, event ):
		event.Skip()

	def m_textCtrl_Track1_AmountOnText( self, event ):
		event.Skip()

	def m_textCtrl_Track1_MonthsOnText( self, event ):
		event.Skip()

	def m_slider_interest_track1OnScrollChanged( self, event ):
		event.Skip()


	def m_choice_track2OnChoice( self, event ):
		event.Skip()

	def m_textCtrl_Track2_AmountOnText( self, event ):
		event.Skip()

	def m_textCtrl_Track2_MonthsOnText( self, event ):
		event.Skip()

	def m_slider_interest_track2OnScrollChanged( self, event ):
		event.Skip()


	def m_choice_track3OnChoice( self, event ):
		event.Skip()

	def m_textCtrl_Track3_AmountOnText( self, event ):
		event.Skip()

	def m_textCtrl_Track3_MonthsOnText( self, event ):
		event.Skip()

	def m_slider_interest_track3OnScrollChanged( self, event ):
		event.Skip()


	def m_choice_track4OnChoice( self, event ):
		event.Skip()

	def m_textCtrl_Track4_AmountOnText( self, event ):
		event.Skip()

	def m_textCtrl_Track4_MonthsOnText( self, event ):
		event.Skip()

	def m_slider_interest_track4OnScrollChanged( self, event ):
		event.Skip()


	def m_CalculateStatsOnButtonClick( self, event ):
		event.Skip()

	def m_create_excel_reportOnButtonClick( self, event ):
		event.Skip()

	def m_menuItem_new_mixOnMenuSelection( self, event ):
		event.Skip()

	def m_menuItem_save_mixOnMenuSelection( self, event ):
		event.Skip()

	def m_menuItem_load_mixOnMenuSelection( self, event ):
		event.Skip()


