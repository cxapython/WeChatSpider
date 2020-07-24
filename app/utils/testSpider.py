# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/24 9:24 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""
import redis
import random
from bs4 import BeautifulSoup
from retrying import retry
import requests
import json
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

@retry(stop_max_attempt_number=5)
def spider_html(url,header):
    print("进行url请求中............")
    if url !="":
        r = requests.get(url=url, headers=header, proxies=get_proxy())
        html = r.text
        # print(html)
        print("爬取页面成功进行页面数据解析中...............")
        soup = BeautifulSoup(html, 'html.parser')
        nickname = soup.find(name='a',attrs={'id': 'js_name'}).text.strip()#微信公众号名称
        title = soup.find(name='div', attrs={'class': 'like_comment_media_title'}) #文章标题
        article_title = title.text.strip()  #文章标题
        spans = soup.find(name='div', attrs={"id": "js_content"}).find_all('span')#文章内容
        images = soup.findAll(name='img', attrs={'class': 'rich_pages', 'data-src': True})
        img_url_list = []
        for image in images:
            img_url_list.append(image['data-src'])
        content = ""
        string_list = []
        for span in spans:
            p = span.text
            string_list.append(p)
        data = content.join(string_list) #处理完的文章内容
        print("页面数据解析完成............准备进行保存数据")
        return article_title,data,url,nickname,json.dumps(img_url_list)