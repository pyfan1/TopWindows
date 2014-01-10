#Boa:Frame:FrameMain
"""
Copyright (c) 2013 David Webster
See license.txt
"""

# The code to get the list of window properties and 
# the isRealWindow() function are taken from here:
# http://stackoverflow.com/questions/151846/get-other-running-processes-window-sizes-in-python

import wx
import os
import win32con
import win32gui
import win32process

def isRealWindow(hWnd):
    '''Return True iff given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def SetListCtrlColumnWidthsHeader(listCtrl):
    for x in xrange(listCtrl.GetColumnCount()):
        listCtrl.SetColumnWidth(x, wx.LIST_AUTOSIZE_USEHEADER)

    for x in xrange(listCtrl.GetColumnCount()):
        listCtrl.SetColumnWidth(x, listCtrl.GetColumnWidth(x) + 3)

def create(parent):
    return FrameMain(parent)

[wxID_FRAMEMAIN, wxID_FRAMEMAINLISTCTRLWINDOWS, wxID_FRAMEMAINPANELTOP, 
] = [wx.NewId() for _init_ctrls in range(3)]

[wxID_FRAMEMAINMENUFILEITEMSEXIT, wxID_FRAMEMAINMENUFILEITEMSREFRESH, 
] = [wx.NewId() for _init_coll_menuFile_Items in range(2)]

class FrameMain(wx.Frame):
    def _init_coll_boxSizerTop_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.listCtrlWindows, 1, border=5,
              flag=wx.EXPAND | wx.ALL)

    def _init_coll_menuBar1_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menuFile, title='&File')

    def _init_coll_menuFile_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAMEMAINMENUFILEITEMSREFRESH,
              kind=wx.ITEM_NORMAL, text='&Refresh\tF5')
        parent.Append(help='', id=wxID_FRAMEMAINMENUFILEITEMSEXIT,
              kind=wx.ITEM_NORMAL, text='E&xit')
        self.Bind(wx.EVT_MENU, self.OnMenuFileItemsrefreshMenu,
              id=wxID_FRAMEMAINMENUFILEITEMSREFRESH)
        self.Bind(wx.EVT_MENU, self.OnMenuFileItemsexitMenu,
              id=wxID_FRAMEMAINMENUFILEITEMSEXIT)

    def _init_coll_listCtrlWindows_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, heading='PID',
              width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading='Width',
              width=-1)
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, heading='Height',
              width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT, heading='Title',
              width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT, heading='Handle',
              width=-1)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizerTop = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizerTop_Items(self.boxSizerTop)

        self.panelTop.SetSizer(self.boxSizerTop)

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.menuFile = wx.Menu(title='')

        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_menuFile_Items(self.menuFile)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAMEMAIN, name='FrameMain',
              parent=prnt, pos=wx.Point(481, 348), size=wx.Size(679, 457),
              style=wx.DEFAULT_FRAME_STYLE, title='Top Windows')
        self._init_utils()
        self.SetClientSize(wx.Size(661, 412))
        self.SetMenuBar(self.menuBar1)

        self.panelTop = wx.Panel(id=wxID_FRAMEMAINPANELTOP, name='panelTop',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(661, 412),
              style=wx.TAB_TRAVERSAL)

        self.listCtrlWindows = wx.ListCtrl(id=wxID_FRAMEMAINLISTCTRLWINDOWS,
              name='listCtrlWindows', parent=self.panelTop, pos=wx.Point(5, 5),
              size=wx.Size(651, 402), style=wx.LC_REPORT)
        self._init_coll_listCtrlWindows_Columns(self.listCtrlWindows)
        self.listCtrlWindows.Bind(wx.EVT_LIST_COL_CLICK,
              self.OnListCtrlWindowsListColClick,
              id=wxID_FRAMEMAINLISTCTRLWINDOWS)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.Title = "Top Windows  (pid %d)" % (os.getpid(),)

        self.window_list = []
        self.sort_column = None
        self.sort_reverse = False
        self.RefreshWindowList()

    def RefreshWindowList(self):
        self.window_list = self.GetTopWindows()
        self.PopulateWindowList()

    def PopulateWindowList(self):
        self.listCtrlWindows.DeleteAllItems()
        if self.sort_column is None:
            for row in self.window_list:
                self.listCtrlWindows.Append(self.RenderColumns(row))
            SetListCtrlColumnWidthsHeader(self.listCtrlWindows)
        else:
            for row in sorted(self.window_list, key=lambda x: x[self.sort_column], 
                                    reverse=self.sort_reverse):
                self.listCtrlWindows.Append(self.RenderColumns(row))
            SetListCtrlColumnWidthsHeader(self.listCtrlWindows)

    def RenderColumns(self, row):
        pid = unicode(row[0])
        width = unicode(row[1])
        height = unicode(row[2])
        title = unicode(row[3], 'cp1252', 'replace')
        handle = unicode(row[4])
        return (pid, width, height, title, handle)

    def GetTopWindows(self):
        """Get list of all top level windows in the system."""
        wl = []
##        wl.append((1, 100, 50, "Some Title", 123456))
##        wl.append((2, 200, 50, "Another Window", 654321))
        def callback(hWnd, windows):
            if not isRealWindow(hWnd):
                return
            _, pid = win32process.GetWindowThreadProcessId(hWnd)
            rect = win32gui.GetWindowRect(hWnd)
            windows.append((pid, rect[2] - rect[0], rect[3] - rect[1],
                    win32gui.GetWindowText(hWnd), hWnd))
        win32gui.EnumWindows(callback, wl)
        return wl

    def OnMenuFileItemsrefreshMenu(self, event):
        self.RefreshWindowList()

    def OnMenuFileItemsexitMenu(self, event):
        self.Close()

    def OnListCtrlWindowsListColClick(self, event):
        sort_col = event.GetColumn()
        if (self.sort_column is not None) and (self.sort_column == sort_col):
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        self.sort_column = sort_col
        self.PopulateWindowList()
