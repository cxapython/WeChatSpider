# -*- encoding:utf-8 -*-
"""
@Time   :   2020/5/20 8:51 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :
"""
from flask import request,jsonify
from . import anlysis
import pymysql
from urllib import parse
import json
from app.utils.parse import parse1
from app.utils.spider import run
@anlysis.route("/getbiz",methods=["GET","POST"])
def getbiz():
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, database='wechatcrawl')
    cursor = conn.cursor()
    sql = "select biz,collect from weixin order by collect asc limit 1"
    cursor.execute(sql)
    bizlist = cursor.fetchone()
    biz = bizlist[0]
    count = bizlist[1]
    times = ""
    if int(count)==0:
        #当前获取到微信公众号采集次数为0次时，设置4小时的时效性，让自动化功能能够充分的获取历史消息内容
        print("当前获取到微信公众号采集次数为0次时，设置长时效性的页面跳转链接.......")
        times = "60000*60*3"
    else:
        times = "60000*30"
    print("选择收集次数最少的公众号进行跳转..........")
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={}".format(biz) + "&scene=124#wechat_redirect"
    print("更新公众号收集的次数.........")
    counts = int(count)+1
    sql2 = "update weixin set collect = {} where biz='{}'".format(counts,biz)
    cursor.execute(sql2)
    conn.commit()
    return "<script>setTimeout(function(){window.location.href='" + url + "';},"+times+");</script>"
@anlysis.route("/getMsgJson",methods=["GET","POST"])
def getMsgJson():
    str = request.values.get('str')
    string = parse.unquote(str)
    JsonStr = {}
    try:
        JsonStr = json.loads(string)
    except Exception as e:
        jstring = "json:" + string
        JsonStr = parse1(jstring)
    lists = JsonStr['list']
    print(lists)
    for list in lists:
        fakeid = list['comm_msg_info']['fakeid']
        type = list['comm_msg_info']['type']
        app_msg_ext_info = list.get('app_msg_ext_info','')
        content_url = ""
        if app_msg_ext_info !='':
            if app_msg_ext_info['content_url'] !="":
                content_url = app_msg_ext_info['content_url']
        conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, database='wechatcrawl')
        cursor = conn.cursor()
        try:
            if content_url!="":
                sql = "insert ignore  into tmplist(content_url,loads)values('{}',{})".format(content_url, 0)
                print("数据正在插入数据库中...............")
                cursor.execute(sql)
                conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    print("保存公众号文章url任务结束.....................")
    # run()
    print("结束微信公众号文章爬取任务！")
    return jsonify("getMsgJson")
@anlysis.route("/getWxPost",methods=["GET","POST"])
def getWxPost():
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, database='wechatcrawl')
    cursor = conn.cursor()
    cursor.execute("select count(*) from tmplist")
    count = cursor.fetchone()
    print("判断队列是否为空")
    if count[0]==0:
        cursor.execute("select biz from weixin order by collect asc limit 1")
        biz = cursor.fetchone()
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={}".format(biz[0])+"&scene=124#wechat_redirect"
        print("将微信公众号历史页面url插入到队列中")
        print(url)
        sql2 = "replace into tmplist(content_url,loads)values('{}',{})".format(url,1)
        cursor.execute(sql2)
        conn.commit()
        print("跳转到微信公众号历史页面...........")
        # print("<script>setTimeout(function(){window.location.href='" + url + "';},2000);</script>")
        return "<script>setTimeout(function(){window.location.href='" + url + "';},2000);</script>"
    else:
        cursor.execute("select content_url from tmplist where loads =0 limit 1")
        urllist = cursor.fetchone()
        url = urllist[0]
        print("队列中存在url内容则跳转到指定的url中.............")
        # print("<script>setTimeout(function(){window.location.href='" + url + "';},2000);</script>")
        return "<script>setTimeout(function(){window.location.href='" + url + "';},2000);</script>"