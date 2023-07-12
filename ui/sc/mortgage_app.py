import sys
sys.path.append(r"C:\Users\dp26422\PycharmProjects\mortgage\ui")
import wx

from oc.template import Mainframe


class MortgageApp(Mainframe):
    def __init__(self, parent):
        super().__init__(parent)
    def m_CalculateStatsOnButtonClick(self, event):
        print("pressed button!")






class MainApp(wx.App):
    def OnInit(self):
        mainFrame = MortgageApp(None)
        mainFrame.Show(True)
        return True

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
