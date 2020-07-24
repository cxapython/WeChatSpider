# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/22 15:13 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""
import requests
import redis
import random
from bs4 import BeautifulSoup
url = "http://mp.weixin.qq.com/s?__biz=MjM5MTUxNTk0MA==&amp;amp;mid=2651460052&amp;amp;idx=1&amp;amp;sn=1f0d5d181b62eaeb09baf350598044d1&amp;amp;chksm=bd4ae59f8a3d6c89b1191ac1c61eed1924f57e32674a24e8f62457f9336ad02213d4c5a4cf6e&amp;amp;scene=27#wechat_redirect"
headers={
    "authority":"mp.weixin.qq.com",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}
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
    print(proxy)
    return proxy
r = requests.get(url,headers=headers,proxies=get_proxy())
html = r.text
soup = BeautifulSoup(html, 'html.parser')
images = soup.findAll(name='img',attrs={'class':'rich_pages','data-src':True})
for image in images:
    print(image['data-src'])