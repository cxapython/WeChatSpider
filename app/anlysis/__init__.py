# -*- encoding:utf-8 -*-
"""
@Time   :   2020/5/20 8:45 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""
from flask import Blueprint
anlysis=Blueprint('anlysis',__name__,url_prefix='/anlysis')
from . import views,errors