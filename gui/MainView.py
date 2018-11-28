
import wx
import GeneralView as gv
import RESView as res

from pubsub import pub
from Events import EVENTS

class MainView ( wx.Frame ):
    
    def __init__(self):
        wx.Frame.__init__(self, None, title="urbs gui 1.0")
        

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        self._nb = wx.Notebook(p)
        self._nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageSelected)
        
        # create the page windows as children of the notebook
        tabOne = gv.GeneralView(self._nb)
        #tabTwo = res.RESView(nb, controller)
        
        # add the pages to the notebook with the label to show on the tab
        self._nb.AddPage(tabOne, "Overview")
        #nb.AddPage(tabTwo, "Ref. Energy Sys.")
        
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(self._nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

    def AddRESTab(self, controller, siteName):
        resTab = res.RESView(self._nb, controller, siteName)        
        self._nb.AddPage(resTab, "Ref. Energy Sys. [" + siteName + "]")
        
    def RemoveRESTab(self, sites):
        for site in sites:
            for i in range(1, self._nb.GetPageCount()):
                if self._nb.GetPage(i).GetSiteName() == site:
                    self._nb.RemovePage(i)
                    break
        
    def OnPageSelected(self, event):
        pageIndx = event.GetSelection()
        if pageIndx == 0: return
        
        resView = self._nb.GetPage(pageIndx)
        pub.sendMessage(EVENTS.RES_SELECTED, siteName=resView.GetSiteName())
    
    def __del__( self ):
        pass


   

