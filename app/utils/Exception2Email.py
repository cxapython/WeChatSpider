# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/24 14:08 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""
from flask_mail import Mail,Message
from flask import Flask,request
from flask_script import Manager,Shell
from threading import Thread
import os
from config import emailConifg
app =Flask(__name__)
app.config['MAIL_SERVER'] = emailConifg.get('MAIL_SERVER')
app.config['MAIL_PORT'] = emailConifg.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = emailConifg.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = emailConifg.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = emailConifg.get('MAIL_PASSWORD')
mail = Mail(app)

def send_message(title,sender,recipient,body,html):
    msg = Message(title,sender=sender,recipients=recipient)
    msg.body = body
    msg.html = html
    print("发送异常信息........")
    mail.send(msg)
    print("发送功能执行完毕")