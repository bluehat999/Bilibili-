# -*- coding: utf-8 -*-
# Version:2018-10-9
# By bluehat999

import datetime
import json
import os
import random
import time
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup as BS
from requests import exceptions

url_view = "https://api.bilibili.com/x/web-interface/view"
url_tags = "https://api.bilibili.com/x/tag/archive/tags"
url_danmaku = "http://comment.bilibili.com/"
url_related = "https://api.bilibili.com/x/web-interface/archive/related"
url_reply = "https://api.bilibili.com/x/v2/reply?type=1"

url_tag_set = "http://api.bilibili.com/x/tag/info?tag_id=1773899"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26\
     Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
}


def get_view(aid):
    """
    获取视频的基本信息
    :param aid: 视频编号
    :return: 视频相关信息的字典
    """
    url = url_view + "?aid=" + str(aid)
    print(url)
    dic = {}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout:
        print("Timeout")
    except exceptions.HTTPError:
        print("HTTPError")
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        if js and js.get('data'):
            data = js.get('data')
            dic['aid'] = data.get('aid')
            dic['title'] = data.get('title')
            dic['desc'] = data.get('desc')
            time_stamp = data.get('pubdate')
            if time_stamp:
                date_array = datetime.datetime.utcfromtimestamp(time_stamp)
                dic['pubdate'] = date_array.strftime("%Y-%m-%d %H:%M:%S")
            else:
                dic['pubdate'] = None
            dic['owner_mid'] = data.get('owner').get('mid')
            dic['owner_name'] = data.get('owner').get('name')
            dic['tname'] = data.get('tname')
            dic['tid'] = data.get('tid')
            dic['pic'] = data.get('pic')

            dic['attribute'] = data.get('attribute')
            dic['coin'] = data.get('stat').get('coin')
            dic['share'] = data.get('stat').get('share')
            dic['favorite'] = data.get('stat').get('favorite')
            dic['view'] = data.get('stat').get('view')
            dic['like'] = data.get('stat').get('like')
            dic['dislike'] = data.get('stat').get('dislike')
            dic['reply'] = data.get('stat').get('reply')
            dic['danmaku'] = data.get('stat').get('danmaku')
            dic['now_rank'] = data.get('stat').get('now_rank')
            dic['his_rank'] = data.get('stat').get('his_rank')

            dic['danmaku_cid'] = data.get('cid')
        #print(dic['aid'])
    return dic


def get_tags(aid):
    """
    获取视频的标签
    :param aid: 视频编号
    :return: 视频标签字典
    """
    url = url_tags + "?aid=" + str(aid)
    dic = {}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout:
        print("Timeout")
    except exceptions.HTTPError:
        print("HTTPError")
    else:
        resp.encoding = resp.apparent_encoding
        data = resp.json().get('data')
        if data:
            # dic['tags_num'] = len(data)
            tags = []
            for tag in data:
                tag_dic = {}
                tag_dic['tag_name'] = tag.get('tag_name').replace("'","").replace('"',"")
                tag_dic['count'] = tag.get('count')
                tags.append(tag_dic)
            dic['tags'] = tags
        #print(dic)
    return dic


def get_related(aid):
    """
    获取推荐的相关视频
    :param aid: 视频编号
    :return: 相关视频的字典
    """
    url = url_related + "?aid=" + str(aid)
    dic = {}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        print(resp.status_code)
    except exceptions.Timeout:
        print("Timeout")
    except exceptions.HTTPError:
        print("HTTPError")
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        if js and js.get('data'):
            data = js.get('data')
            str_related = ""
            for rela in data:
                str_related = str_related + str(rela.get('aid')) + ","
            dic['related'] = str_related
    return dic


def get_danmaku(aid, cid):
    """
    获取视频弹幕并保存为以视频编号命名的文件
    :param aid: 视频编号
    :param cid: 弹幕编号
    :return: None
    """
    url = url_danmaku + str(cid) + ".xml"
    path = "VideosData/Danmaku/" + str(aid) + ".txt"
    file = open(path, 'w', encoding='UTF-8')
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout:
        print("Timeout")
    except exceptions.HTTPError:
        print("HTTPError")
    else:
        resp.encoding = resp.apparent_encoding
        xml = resp.text
        soup = BS(xml, 'xml')
        #print(soup.text)
        danmakus = soup.find_all(name='d')
        for d in danmakus:
            file.write(d.text + "\n")
    file.close()


def get_reply(aid):
    """
    获取用户的评论信息，并保存到用视频编号命名的文件中
    :param aid: 视频编号
    :return: None
    """
    url = url_reply + "&oid=" + str(aid)
    path = "VideosData/Reply/" + str(aid) + ".txt"
    file = open(path, 'w', encoding='UTF-8')
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
    except exceptions.Timeout:
        print("Timeout")
    except exceptions.HTTPError:
        print("HTTPError")
    else:
        resp.encoding = resp.apparent_encoding
        js = resp.json()
        if js and js.get('data'):
            replies = js.get('data').get('replies')
            for reply in replies:
                file.write(str(reply.get('mid')) + " says: " + reply.get('content').get('message') + "\n")
    file.close()


def get_all(aid):
    dic = get_view(aid)
    if dic:
        dic1 = get_tags(aid)
        for k, v in dic1.items():
            dic[k] = v
        dic1 = get_related(aid)
        for k, v in dic1.items():
            dic[k] = v
        '''
        if dic.get('danmaku'):
            get_danmaku(aid, dic.get('danmaku_cid'))
        if dic.get('reply'):
            get_reply(aid)
        '''
        print(">>>>>>>>>>>>>>>>>>>>>" + str(aid) + "号视频信息已成功获取<<<<<<<<<<<<<<<<<<<<\n\n")
    else:
        print(">>>>>>>>>>>>>>>>>>>>>" + str(aid) + "号视频不存在或者已下架<<<<<<<<<<<<<<<<<<<<\n\n")
    return dic


def storage(dic, index):
    file = open("VideosData/Video/video" + str(index) + ".txt", 'a', encoding='utf-8')
    json.dump(dic, file, ensure_ascii=False, sort_keys=True)
    file.write(",\n")
    return None


def video_spider(index):
    with open("VideosData/startaid" + str(index), 'r') as f:
        start_mid = int(f.read())
    while start_mid < (index + 1) * 10000000:
        try:
            dic = get_all(start_mid)
            if dic:
                storage(dic, index)
        except AttributeError:
            start_mid += random.randint(5, 30)
            continue
        else:
            start_mid += random.randint(0, 60)
            with open("VideosData/startaid" + str(index), 'w') as f:
                f.write(str(start_mid))
            time.sleep(0.1)

'''
if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(4):
        p.apply_async(video_spider, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.') 
'''
# video_spider(0)
