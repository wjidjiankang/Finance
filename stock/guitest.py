# import wxPython as wx
#
# import wx

import wx                               #导入wx包
app = wx.App()                          #创建应用程序对象
win = wx.Frame(None,-1,'install test')  #创建窗体
btn = wx.Button(win, label = 'Button')  #创建Button
win.Show()                              #显示窗体
app.MainLoop()