# -*- encoding:utf-8 -*-
"""
@Time   :   2020/7/22 8:50 
@Author :   yanyu
@Email  :   973900834@qq.com
@Project:   
@Description    :   
"""


def skip_ws(txt, pos):
    while pos < len(txt) and txt[pos].isspace():
        pos += 1
    return pos


def parse_str(txt, pos, allow_ws=False, delimiter=[',', ':', '}', ']']):
    while pos < len(txt):
        if not allow_ws and txt[pos].isspace():
            break
        if txt[pos] in delimiter:
            break
        pos += 1
    return pos


def parse_obj(txt, pos):
    obj = dict()

    while True:
        pos = skip_ws(txt, pos + 1)
        end = parse_str(txt, pos, True, [':'])
        if end >= len(txt):
            raise ValueError("unexpected end when parsing object key")
        key = txt[pos:end].strip()
        pos = skip_ws(txt, end + 1)
        if pos >= len(txt):
            raise ValueError("unexpected end when parsing object value")
        if txt[pos] == '[':
            value, pos = parse_array(txt, pos)
        elif txt[pos] == '{':
            value, pos = parse_obj(txt, pos)
        else:
            end = parse_str(txt, pos, True, [',', '}'])
            if end >= len(txt):
                raise ValueError("unexpected end when parsing object value")
            value = txt[pos:end].strip()
            pos = end

        obj[key] = value
        pos = skip_ws(txt, pos)
        if pos >= len(txt):
            raise ValueError("unexpected end when object value finish")
        if txt[pos] == '}':
            return obj, pos + 1


def parse_array(txt, pos):
    array = list()

    while True:
        pos = skip_ws(txt, pos + 1)
        if pos >= len(txt):
            raise ValueError("unexpected end when parsing array item")
        if txt[pos] == '[':
            value, pos = parse_array(txt, pos)
        elif txt[pos] == '{':
            value, pos = parse_obj(txt, pos)
        else:
            end = parse_str(txt, pos, True, [',', ']'])
            if end >= len(txt):
                raise ValueError("unexpected end when parsing array item")
            value = txt[pos:end].strip()
            pos = end

        array.append(value)
        pos = skip_ws(txt, pos)
        if pos >= len(txt):
            raise ValueError("unexpected end when array item finish")
        if txt[pos] == ']':
            return array, pos + 1


def parse1(txt):
    if txt.startswith('json'):
        pos = txt.find(':')
        if pos != -1:
            pos = skip_ws(txt, pos + 1)
            if txt[pos] == '{':
                obj, pos = parse_obj(txt, pos)
                return obj
            elif txt[pos] == '[':
                array, pos = parse_array(txt, pos)
                return array
    raise ValueError("format error when parsing root")


if __name__ == '__main__':
    txt = "json:{list:[{comm_msg_info:{id:1000013605,type:49,datetime:1595377477,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:全球10例，他第一个出院,digest:,content:,fileid:509445139,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928841&amp;amp;idx=1&amp;amp;sn=6c0ecb5f2843ec39f5a5dc141e50edab&amp;amp;chksm=7a6779af4d10f0b9efee9efde1b8b4dd69e6d2142acf98a9b93ed86095c87694c90b1e18f4de&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGU2dKfDlOBNghNfs4DqIyiaicHHoQE3tXyS8srmfpKttqhbK4biaAsk9o8g/0?wx_fmt=jpeg,subtype:9,is_multi:1,multi_app_msg_item_list:[{title:这些都是假的，别信→,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928841&amp;amp;idx=2&amp;amp;sn=d8fd45d1ec88e30e3f8b6c5a45d830ad&amp;amp;chksm=7a6779af4d10f0b94c71c9ebbae5e8c4698c86d4119ae8459ae0dc61db6735d79127a5ccf27d&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUGxuDlrMugppcU199POT6BN7GckSogTrKaqrxqXplYcVUGXc2fHh6WA/0?wx_fmt=jpeg,author:,copyright_stat:100,del_flag:1,item_show_type:0,audio_fileid:0,duration:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013604,type:49,datetime:1595374771,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:那名想上《新闻联播》的火箭军战士不简单，他的真实身份是……,digest:,content:,fileid:509445170,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928825&amp;amp;idx=1&amp;amp;sn=0f20b130ab8dbef36a6a2f5e73fbecb2&amp;amp;chksm=7a6779df4d10f0c97b7d5d3006a68090894c7b58d1cd8412da9071e999ee711ec523ac2c261c&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUlzkEhFfpNHvMia6BZzrFTegpNYicGWGTfXXGiaN4atvulZaF7gmLRUeqg/0?wx_fmt=jpeg,subtype:9,is_multi:1,multi_app_msg_item_list:[{title:货车司机1小时被连开4张罚单？！涉事警察停职调查,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928825&amp;amp;idx=2&amp;amp;sn=c56f76aebe49f677d91206d921f3021c&amp;amp;chksm=7a6779df4d10f0c95d0f47f633da96ac872dcb188c6d9399dfaa642c0f1866610930e5785d80&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUSDMQJwutAajQyaajF7WmOSlOhgicqEb8jzKrnz17DHVq1gm2RI9mQ1A/0?wx_fmt=jpeg,author:,copyright_stat:100,del_flag:1,item_show_type:0,audio_fileid:0,duration:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013603,type:49,datetime:1595371723,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:最热྆热྆热྆热྆热྆的时候来了~,digest:,content:,fileid:509445004,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928821&amp;amp;idx=1&amp;amp;sn=02b4cbc56900c52629e50faa486891f8&amp;amp;chksm=7a6779d34d10f0c5a3238b36919fa6907e43bce57feb98857775b41c767aeb7fc27c18c07e5d&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUMNnC9kTb0yazqVbW7lb0Bu3cGXN8rG3iajnYWeIAqyqEJibiaTR9Tic2JQ/0?wx_fmt=jpeg,subtype:9,is_multi:0,multi_app_msg_item_list:[],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013602,type:49,datetime:1595367172,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:早啊！新闻来了〔2020.07.22〕,digest:○习近平主持召开企业家座谈会并发表重要讲话\\n○淮河干流王家坝段水位退至保证水位\\n○每年1月10日为“中国人民警察节”\\n○专家：新发地相关疫情及传播扩散已全部终止​,content:,fileid:509445049,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928813&amp;amp;idx=1&amp;amp;sn=aa4a929101b88dd34afd15685cc9e5b5&amp;amp;chksm=7a6779cb4d10f0dd18a4706adcf428f5d177c05fce1712c49e1af52fb337384979ce38ef78fc&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUwVfCic1BmJaEwcjXqFcDOSe0BnvZdwDArlv7noTJkNt2y3ng5ugE4ow/0?wx_fmt=jpeg,subtype:9,is_multi:0,multi_app_msg_item_list:[],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013601,type:49,datetime:1595344947,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:主播说联播&nbsp;|&nbsp;习近平今天主持一个重磅座谈会，海霞：与会代表名单本身就有信息量,digest:,content:,fileid:509445059,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928729&amp;amp;idx=1&amp;amp;sn=90599665d3a1d15e02db7ec47f674d6b&amp;amp;chksm=7a677e3f4d10f729f53ea8d514a6b356f04029c88bcfdc7845eba0c9a560c5ddadc9fc702acd&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUrdlGJagQXUpdssrlsrpnvoQrw6gx16X9f5SaNeBzkNx4DTSYfGsk6Q/0?wx_fmt=jpeg,subtype:9,is_multi:0,multi_app_msg_item_list:[],author:新闻联播,copyright_stat:101,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013600,type:49,datetime:1595340568,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:夜读丨大暑：轻罗小扇扑流萤,digest:7月22日16时37分，迎来夏季最后一个节气“大暑”。,content:,fileid:509444954,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928684&amp;amp;idx=1&amp;amp;sn=09b2c86677d0ae59b58b1bda93a04a11&amp;amp;chksm=7a677e4a4d10f75c587a676dae944c0145622cd3b8c547cb160a775e48842694ff2397f063fd&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUs2tutxHyPKVItyqQbx5XTuUpBeTI4cB9nhRR2NCW2Pjt4dmbgBqSfw/0?wx_fmt=jpeg,subtype:9,is_multi:0,multi_app_msg_item_list:[],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013599,type:49,datetime:1595335691,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:警报再次拉响！湖北恩施山体大面积滑移，已形成堰塞湖,digest:,content:,fileid:509444849,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928620&amp;amp;idx=1&amp;amp;sn=66ce3edbba045eb67d456ce503b63b44&amp;amp;chksm=7a677e8a4d10f79c5baa8e0c1a17433079510c12a518ac78744e6acc873838d452e012f610c8&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUne1EKeGjfYNXibnvXrhTkq4xIYtWlWv1vYbzHYfUwh3RNz0m5Idpzjw/0?wx_fmt=jpeg,subtype:9,is_multi:1,multi_app_msg_item_list:[{title:北斗又出手了！,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928620&amp;amp;idx=2&amp;amp;sn=637330777a5f3eeabc8623c4e326371c&amp;amp;chksm=7a677e8a4d10f79cb11016f04ee374f69852cbd8a59121a6cffa974354aab6992a1e5b04494a&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUricmYSaibvYJ53XBITQDJVgq7E06H2bBHar8vkN029S3cBf9icnSLtOGA/0?wx_fmt=jpeg,author:,copyright_stat:100,del_flag:1,item_show_type:0,audio_fileid:0,duration:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013598,type:49,datetime:1595330085,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:这两地，都有好消息！,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928531&amp;amp;idx=1&amp;amp;sn=99143d920b06a733577a0a3b04d9bce2&amp;amp;chksm=7a677ef54d10f7e3b25145960dab21bdf05ee7626a8fb827e1fc203b441724fea995c6a8bbac&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUFlPjhm95n1icoPB8wyPtHN34tymJ74VSvp8ITExC9TNYdCtO4PtyYmA/0?wx_fmt=jpeg,subtype:9,is_multi:1,multi_app_msg_item_list:[{title:外交部辟谣！,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928531&amp;amp;idx=2&amp;amp;sn=632a4d0ed732beb418ef60e3120b82a2&amp;amp;chksm=7a677ef54d10f7e33e6484c34d5fa28afa3d953dfa2908ba14f6a90a4313d42d893bcdc2ca2f&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUTEibwZWqqywf3xMKhiadSn1Kc9fI7lorEZ0Um8safNzwmnJUPBULKEow/0?wx_fmt=jpeg,author:,copyright_stat:100,del_flag:1,item_show_type:0,audio_fileid:0,duration:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013597,type:49,datetime:1595321994,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:好暖啊！洪水来了，老两口第一时间搬的是……,digest:,content:,fileid:509444776,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928455&amp;amp;idx=1&amp;amp;sn=1a464d7a9a2f06fd678f69aa41312544&amp;amp;chksm=7a677f214d10f637851cfde9a6af38434904a99b085cee4badabd41b8f4a348af3e3b4fb0a4a&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUanOGCAd3ojyTHDHj3NxgiaBJOong7haNUSEItE8bSY7tXEOnA6da5Fw/0?wx_fmt=jpeg,subtype:9,is_multi:1,multi_app_msg_item_list:[{title:新版清华录取通知书出炉，太美了！我又酸了,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928455&amp;amp;idx=2&amp;amp;sn=5e726ef2ae681026151738cc04ef2073&amp;amp;chksm=7a677f214d10f637d12787d81baf09d024f3d72b454f16a964b98888957f512cbc76c2b2ef66&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUYZqItLw55IY7t26hkWS6IH7YLsPFh5x28c2hOicbBaZdGODTjpbI7Zw/0?wx_fmt=jpeg,author:,copyright_stat:100,del_flag:1,item_show_type:0,audio_fileid:0,duration:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}},{comm_msg_info:{id:1000013596,type:49,datetime:1595312452,fakeid:1240574601,status:2,content:},app_msg_ext_info:{title:全网都在感谢他们！请记住这个名字：王家坝,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928376&amp;amp;idx=1&amp;amp;sn=9a55b75c31797b190f839b2564a8fe80&amp;amp;chksm=7a677f9e4d10f688705bce075e30894bc3adb71109da26ed145523dc04d5b3a0c79f98529ac8&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUdFAyvG5RPccZupg5Tpwib4iamIMXSiapicRrBMtAA6pDKAQoZ5ibww7jXXQ/0?wx_fmt=jpeg,subtype:9,is_multi:1,multi_app_msg_item_list:[{title:重要调整！涉及来华航班→,digest:,content:,fileid:0,content_url:http://mp.weixin.qq.com/s?__biz=MTI0MDU3NDYwMQ==&amp;amp;mid=2656928376&amp;amp;idx=2&amp;amp;sn=535d1d28a11cd6057a89442d07acdbf7&amp;amp;chksm=7a677f9e4d10f68886b0f63b03e54acf2fe1619f1780c943013b0dc8b31b2aab4488c016e7bd&amp;amp;scene=27#wechat_redirect,source_url:,cover:http://mmbiz.qpic.cn/mmbiz_jpg/oq1PymRl9D7Wia7FUVJiawJHNVDmWQEtGUXzkZqgGEl4peq8hMSDx9YK3rGabGlmuu7d54Y5zg2Ixr6MkQxyWDqA/0?wx_fmt=jpeg,author:,copyright_stat:100,del_flag:1,item_show_type:0,audio_fileid:0,duration:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}],author:,copyright_stat:100,duration:0,del_flag:1,item_show_type:0,audio_fileid:0,play_url:,malicious_title_reason_id:0,malicious_content_type:0}}]}"
    print(parse1(txt))