
import wx
import GeneralView as gv
import RESView as res

class MainView ( wx.Frame ):
    
    def __init__( self ):
        wx.Frame.__init__(self, None, title="urbs gui 1.0")

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        
        # create the page windows as children of the notebook
        tabOne = gv.GeneralView(nb)
        tabTwo = res.RESView(nb)
        
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(tabOne, "Overview")
        nb.AddPage(tabTwo, "Ref. Energy Sys.")
        
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

    
    def __del__( self ):
        pass


   

