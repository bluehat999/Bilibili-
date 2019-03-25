# -*- coding: utf-8 -*-
#Version:2019-03-05
#By bluehat999

import requests, random, requests, json, time, datetime,sys
from requests import exceptions
import Video_Spider
import ciyun
url1 = "https://space.bilibili.com/ajax/member/GetInfo"     #method=post，基本信息
url2 = "https://space.bilibili.com/ajax/member/getTags?mids="      #method=get，用户标签
url3 = "https://api.bilibili.com/x/space/navnum?jsonp=jsonp&callback=__jp2&mid="      #method=get,视频数目
url4 = "https://api.bilibili.com/x/relation/stat?jsonp=jsonp&callback=__jp2&vmid="     #method=get,关注数和粉丝数
url5 = "https://api.bilibili.com/x/space/upstat?jsonp=jsonp&callback=__jp3&mid="       #method=get,播放数和阅读数
url6 = "https://api.bilibili.com/x/relation/followings?order=desc&jsonp=jsonp&callback=__jp10&vmid="
url7 = "https://api.bilibili.com/x/relation/followers?order=desc&jsonp=jsonp&callback=__jp11&vmid=" #粉丝
url8 = "https://api.bilibili.com/x/space/fav/nav?jsonp=jsonp&callback=__jp11&mid=" #收藏夹
url9 = "https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id="#收藏夹列表
url10 = "https://space.bilibili.com/ajax/Bangumi/getList?page=1&mid="    #订阅列表
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6721.400 QQBrowser/10.2.2243.400",
           'Referer': ''
           }
storage_path="UsersData/users0.55.txt"

def getheaders():
    return None
# {"status":False,"data":""}
#0
def getall(mid):
    dic_basic = get_basic_info(mid)
    dic_tag = get_tags_info(mid)
    dic_o = get_other_info(mid)
    for k, v in dic_tag.items():
        dic_basic[k] = v
    for k, v in dic_o.items():
        dic_basic[k] = v
    dic1 = {}
    dic1['data'] = dic_basic
    dic1['status'] = "true"
    return dic1
#基本信息
def get_basic_info(mid):
    dic = {}
    headers['Referer'] = "https://space.bilibili.com/"+str(mid)+"/"            #该条头部信息必须有
    try:
        response = requests.post(url1, data={"mid": str(mid)}, timeout=5, headers=headers)
        response.raise_for_status()
    except exceptions.Timeout as e:
        return({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return({"status":"false","data":"HTTPError"+response.status_code+response.headers})
    else:
        response.encoding = response.apparent_encoding
        js = response.json()
        if not js.get('status'):
            return ({"status":"false","data":"get_basic_info error"})
        dic['mid'] = js.get('data').get('mid')
        dic['name'] = js.get('data').get('name')
        dic['sex'] = js.get('data').get('sex')
        dic['face'] = js.get('data').get('face')
        timeStamp = js.get('data').get('regtime')
        if timeStamp != None:
            dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
            dic['regtime'] = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        else:
            dic['regtime'] = None
        dic['birthday'] = js.get('data').get('birthday')
        dic['sign'] = js.get('data').get('sign')
        dic['level'] = js.get('data').get('level_info').get('current_level')
        if dic['level']==None:
            dic['level']=-1
        dic['coins']=js.get('data').get('coins')
        dic['official_verify']=js.get('data').get('official_verify').get('desc')
    return dic
#标签信息
def get_tags_info(mid):
    dic={}
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get( url2+str(mid), headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout as e:
        return({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        s = ""
        for tag in js.get('data')[0].get('tags'):
            s =s + tag + ","
        dic['tags'] = s
    return dic
#活跃信息
def get_other_info(mid):
    dic = {}
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get(url3+str(mid), headers=headers, timeout=5)
        r4 = requests.get(url4+str(mid), headers=headers, timeout=5)
        r5 = requests.get(url5 + str(mid), headers=headers, timeout=5)
        resp.raise_for_status()
        r4.raise_for_status()
        r5.raise_for_status()
    except exceptions.Timeout as e:
        return({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = json.loads(resp.text[6:-1])
        dic['video']=js.get('data').get('video')
        js = json.loads(r4.text[6:-1])
        if js.get('code') ==0:
            dic['following'] = js.get('data').get('following')
            dic['follower'] = js.get('data').get('follower')
        js = json.loads(r5.text[6:-1])
        if js.get('code') ==0:
            dic['archive_view'] = js.get('data').get('archive').get('view')
            dic['article_view'] = js.get('data').get('article').get('view')
    return dic
#关注人员列表2
def get_followings_list(mid, ps=50, pn=1):
    l=[]
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get(url6 + str(mid), headers=headers, timeout=5,params={"ps": ps, "pn": pn}) #每次最多获取50项
        resp.raise_for_status()
    except exceptions.Timeout as e:
        return ({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return ({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = json.loads(resp.text[7:-1])
        li = js.get('data').get('list')
        for i in li:
            dic={}
            dic['mid'] = i['mid']
            dic['name'] = i['uname']
            l.append(dic)
        dic1 = {}
        dic1['status'] = "true"
        dic1['data'] = l
    return dic1
#粉丝列表3
def get_followers_list(mid, ps=50, pn=1):
    l=[]
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get(url7 + str(mid), headers=headers, timeout=5,params={"ps": ps, "pn": pn})
        resp.raise_for_status()
    except exceptions.Timeout as e:
        return ({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return ({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = json.loads(resp.text[7:-1])
        li = js.get('data').get('list')
        for i in li:
            dic={}
            dic['mid'] = i['mid']
            dic['name'] = i['uname']
            l.append(dic)
        dic1 = {}
        dic1['status'] = "true"
        dic1['data'] = l
    return dic1
#收藏夹4
def get_collection(mid,ps=20,pn=1):
    dic={}
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get( url8+str(mid), headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout as e:
        return ({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return ({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = json.loads(resp.text[7:-1])
        if js.get('code')!=0:
            return ({"status":"false","data":"get_collection error"})
        archive = js.get('data').get('archive')
        all_list = []
        # media_id = []
        for a in archive:
            if a:
                all_list += get_medialist(a.get('media_id'),mid,ps,pn)
        tags = ""
        for it in all_list:
            if it.get('tags'):
                for tag in it.get('tags'):
                # print(tags)
                    tags += tag['tag_name']+" "
        if tags != "":#将不相关的输出重定向
            f=open('a.txt','w')
            old=sys.stdout #将当前系统输出储存到临时变量
            sys.stdout=f   #输出重定向到文件
            ciyun.draw_wordcloud(tags,mid)  #测试一个打印输出
            sys.stdout=old     #还原系统输出
            f.close()
        dic1 = {}
        dic1['status'] = "true"
        dic1['data'] = all_list
    return dic1

def get_medialist(media_id,mid,ps=20,pn=1):
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get( url9+str(media_id), headers=headers, timeout=5,params={"ps":ps,"pn":pn})
        resp.raise_for_status()
    except exceptions.Timeout as e:
        return ({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return ({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        if js.get('code')!=0:
            return {"status":"false","data":"get_medialist %i error"%media_id}
        list1 = []
        dic = {}
        medialist = js.get('data').get('medias')
        if medialist is None:
            return []
        for item in medialist:
            dic = {}
            dic['aid'] = item.get('id')
            dic['title'] = item.get('title').replace("'","").replace('"',"") #放入字典中时先去点内部的单引号、双引号，以免打印出非标准的json字符串
            # dic['intro'] = item.get('intro')
            dic_tag = Video_Spider.get_tags(item.get('id'))
            for k, v in dic_tag.items():
                dic[k] = v
            list1.append(dic)
    return list1

def get_bangumi(mid,ps=50,pn=1):
    headers['Referer'] = "https://space.bilibili.com/" + str(mid) + "/"
    try:
        resp = requests.get(url10 + str(mid), headers=headers, timeout=5,params={"ps":ps,"pn":pn})
        resp.raise_for_status()
    except exceptions.Timeout as e:
        return ({"status":"false","data":e})
    except exceptions.HTTPError as e1:
        return ({"status":"false","data":"HTTPError"+resp.status_code+resp.headers})
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        if not js.get('status'):
            return {"status":"false","data":"get bangumi error"}
        bangumi_list = []
        for item in js.get('data').get('result'):
            item_dic={}
            item_dic['title'] = item.get('title')
            item_dic['url'] = item.get('share_url')
            bangumi_list.append(item_dic)
        dic1 = {}
        dic1['status'] = "true"
        dic1['data'] = bangumi_list
    return dic1

def storage(dic):
    file = open(storage_path, 'a',encoding='utf-8')
    json.dump(dic, file, ensure_ascii = False, sort_keys = True, indent =4)
    file.write(",\r")
    return None

def user_spider():
    with open("UsersData/startmid0",'r') as f:
        start_mid = int(f.read())
    while start_mid < 100000000:
        try:
            storage(getall(start_mid))
        except AttributeError :
            start_mid +=random.randint(10,100)
            continue
        else:
            start_mid += random.randint(0, 200)
            with open("UsersData/startmid0", 'w') as f:
                f.write(str(start_mid))
            time.sleep(0.1)

# user_spider()
# print(get_followings_list(1314125))

# 重新定义标准输出
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


# print(sys.argv,sys.argv[2])
if int(sys.argv[2])==0:
    print(getall(int(sys.argv[1])))
elif int(sys.argv[2])==1:
    print()
elif int(sys.argv[2])==2:
    print(get_followings_list(int(sys.argv[1]),ps=50,pn=int(sys.argv[3])))
elif int(sys.argv[2])==3:
    print(get_followers_list(int(sys.argv[1]),ps=50,pn=int(sys.argv[3])))
elif int(sys.argv[2])==4:
    print(get_collection(int(sys.argv[1]),ps=20,pn=int(sys.argv[3])))
    # get_collection(int(sys.argv[1]),ps=20,pn=int(sys.argv[3]))
elif int(sys.argv[2])==5:
    print(get_bangumi(int(sys.argv[1]),ps=50,pn=int(sys.argv[3])))
else:
    print("error argv")
