import datetime
import json
import os
import random
import time
import requests
import pymysql
from multiprocessing import Pool
from requests import exceptions

file = 'tid.json'
url_tag_set = "http://api.bilibili.com/x/tag/info"
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; ServiceUI 13.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
     'Host': 'api.bilibili.com',

}
db = pymysql.connect("134.175.205.95","root","712srxsj","bilibili" )
cursor = db.cursor()

def get_tag(tid):
    """
    获取一条标签信息
    :param tid: 视频编号
    :return: 标签相关信息的字典
    """
    func_re = {"status":0,"data":""}
    url = url_tag_set + "?tag_id=" + str(tid)
    try:
        headers['User-Agent'] = random.choice(my_headers)
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout:
        func_re['status']=3
        return func_re
    except exceptions.HTTPError as e:
        func_re['status']=4
        print(url,e.response)
        return func_re
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        # print(js)
        if js.get('code') != 0:
            return func_re
        data_dic = {}
        data_dic["tag_id"] = js.get('data').get('tag_id')
        data_dic["name"] = js.get('data').get('tag_name')
        data_dic["use"] = js.get('data').get('count').get('use')
        data_dic["atten"] = js.get('data').get('count').get('atten')
        data_dic["view"] = js.get('data').get('count').get('view')
        data_dic["content"] = js.get('data').get('content')
        if data_dic['use']+3*data_dic['view']+data_dic['view']<100:
            return func_re
        # print(data_dic["tag_id"])
        func_re['status'] = 1
        func_re['data'] = data_dic          
    return func_re
def putTagDb(item):
    sql1 = "select tagId from tags where tagId=%d"%int(item.get('tag_id'))
    #使用了sql关键词use，需要加``
    sql2 = "insert into tags (tagId,name,`use`,atten,view,content)\
            values(%d,'%s',%d,%d,%d,'%s')"%\
                (int(item.get('tag_id')),pymysql.escape_string(item.get('name')),\
                int(item.get('use')),int(item.get('atten')),int(item.get('view')),\
                pymysql.escape_string(item.get('content')))
    # print(sql2)
    cursor.execute(sql1)
    data = cursor.fetchone()
    if data:
        return 0
    cursor.execute(sql2)
    db.commit()
    return 1
if __name__ == "__main__":
    with open(file,'r') as fp:
        # print(fp.readline())
        fp_json = json.load(fp)
        tid0 = int(fp_json.get('tid0'))
        tid1 = int(fp_json.get('tid1'))

    while tid0<1000000:
        resp = get_tag(tid0)
        # print(tid0,resp)
        if resp.get('status')==1:
            # print(resp)
            putTagDb(resp.get('data'))
            fp_json['tid0']=tid0
            print(tid0)
            with open(file,'w') as fpw:
                fpw.write(str(fp_json).replace("'",'"'))
        tid0 +=1
        time.sleep(0.2)

    
    
#!/usr/bin/python3
