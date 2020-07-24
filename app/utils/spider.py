# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/21 14:56 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""
import re
import requests
from bs4 import BeautifulSoup
import redis
import random
import pymysql
from concurrent.futures import ThreadPoolExecutor,as_completed
from retrying import retry
import json
import time
from .Exception2Email import send_message
from config import emailConifg
def get_proxy():
    print("获取代理ip中")
    pool = redis.ConnectionPool(host='10.2.13.251', port=6379, password='pszxredis', db=0)
    r = redis.StrictRedis(connection_pool=pool)
    datalist = r.getrange('redis_dic', 0, -1)
    datalist = eval(datalist)
    proxylist = list(datalist.keys())
    proxy_list = []
    proxy_dic = {}
    for proxy in proxylist:
        proxy_dic['http'] = proxy
        proxy_list.append(proxy_dic)
    proxy = random.choice(proxy_list)
    return proxy
def insert_data(title,article,url,nickname,image):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        sql = "replace into article(nickname,title,content,img_url,web_url)values('{}','{}','{}','{}','{}')".format(nickname,title,article,image,url)
        # print(sql)
        print("插入爬取的文章内容.................")
        cursor.execute(sql)
        conn.commit()
        print("文章内容插入成功！")
    except Exception as e:
        print(e)
headers={
    "authority":"mp.weixin.qq.com",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}
@retry(stop_max_attempt_number=5)
def spider_html(url,header):
    print("进行url请求中............")
    if url !="":
        try:
            r = requests.get(url=url, headers=header, proxies=get_proxy())
            html = r.text
            # print(html)
            print("爬取页面成功进行页面数据解析中...............")
            soup = BeautifulSoup(html, 'html.parser')
            nicknames = soup.find(name='a', attrs={'id': 'js_name'})  # 微信公众号名称
            if nicknames is not None:
                nickname = nicknames.text.strip()
            else:
                nicknames = soup.find(name='strong', attrs={'class': 'account_nickname_inner account_nickname_inner js_go_profile'})
                nickname  = nicknames.text.strip()
            title = soup.find(name='div', attrs={'class': 'like_comment_media_title'})  # 文章标题
            if title is not None:
                article_title = title.text.strip()  # 文章标题
            else:
                title = soup.find(name='h2', attrs={'class': 'common_share_title js_video_channel_title'})  # 文章标题
                if title is None:
                    article_title = ""
                else:
                    article_title = title.text.strip()  # 文章标题
            spans = soup.find(name='div', attrs={"id": "js_content"}).find_all('span')  # 文章内容
            if spans is not None:
                content = ""
                string_list = []
                for span in spans:
                    p = span.text
                    string_list.append(p)
                data = content.join(string_list)  # 处理完的文章内容
            else:
                data = ""
            images = soup.findAll(name='img', attrs={'class': 'rich_pages', 'data-src': True})
            img_url_list = []
            if images is not None:
                for image in images:
                    img_url_list.append(image['data-src'])
            print("页面数据解析完成............准备进行保存数据")
            return article_title, data, url, nickname, json.dumps(img_url_list)
        except Exception as e:
            print(e)
            html = "<b>"+str(e)+"</b>"
            #发送异常信息邮件到我的qq邮箱
            send_message('微信文章页面数据爬取解析失败',emailConifg.get('MAIL_USERNAME'),'973900834@qq.com',str(e),html)
            update_loads_exp(url)
def update_loads(url):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        print("更新url的爬取状态") #0未爬取 1已爬取 2爬取异常
        sql = "update tmplist set loads=1 where content_url ='{}'".format(url)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
def update_loads_exp(url):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        print("更新url的爬取状态") #0未爬取 1已爬取 2爬取异常
        sql = "update tmplist set loads=3 where content_url ='{}'".format(url)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def get_conn():
    conn = pymysql.connect(host="localhost", user="root", password="root", port=3306, database='wechatcrawl')
    return conn
def run():
    conn = get_conn()
    cursor = conn.cursor()
    sql = "select content_url from tmplist where loads=0 limit 100"
    cursor.execute(sql)
    url_list = cursor.fetchall()
    if len(url_list)==0:
        print("静默10分钟，等待爬取的url链接......")
        time.sleep(60*10)
        run()
    else:
        results = []
        taskList = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for url in url_list:
                print("开启多线程任务......url为:"+str(url[0]))
                task = executor.submit(spider_html, url[0],headers)
                taskList.append(task)
            else:
                print("进行任务解析..........")
                for task in as_completed(taskList):
                    item = task.result()
                    #item[0] 文章标题 #item[1] 文章内容 #item[2]文章url # item[3]公众号 #item[4]图片路径
                    if item is not None:
                        insert_data(item[0],item[1],item[2],item[3],item[4])
                        update_loads(item[2])

if __name__ == '__main__':
    while True:
        run()





