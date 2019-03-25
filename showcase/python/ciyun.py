# -*- coding: utf-8 -*-
__author__ = 'leilu'
#wordcloud生成中文词云

from wordcloud import WordCloud
import codecs
import jieba
#import jieba.analyse as analyse
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


# 绘制词云
def draw_wordcloud(comment_text,mid):
    #读入一个txt文件
    # comment_text = "乐评盘点 王嘉尔安静 开口脆 神仙翻唱 吴青峰起风了 张靓颖翻唱东西 起风了 东西 明星翻唱 网红歌曲翻唱 鬼畜 党妹 洗脑 鬼畜调教 蜜汁带感 机智的党妹 综艺 谢楠 吴京 非常静距离 国内综艺 YouTube搬运 同性 Nick Horton Brick Brandon Szczupaj 科幻 人性 烧脑 小成本 电影解读 美妆 化妆教程 彩妆 教程 明星 张云雷 宁天 天天 日向宁次 粘着系男子の15年ネチネチ 自制 火影忍者 泪腺崩坏 作者是神仙 数码 IPAD 苹果 IPADPRO 笔记 ipad 演奏 没人能在我的BGM里战胜我 上海彩虹室内合唱团 薛定谔的春节 上春晚 春节自救指南 年度神曲第三季 逢年过节必备 金承志 不火没道理 交响乐 合唱 李栋旭 电视剧 韩剧 刘仁娜 金高银 孔刘 鬼怪 孤独灿烂的神鬼怪 刘仁娜 陆星材 李栋旭 剪辑 金高银 孔刘 鬼怪 釜山行 孤单又灿烂的神-鬼怪 李栋旭 刘仁娜 陆星材 金高银 鬼怪 孔刘 孤单又灿烂的神-鬼怪 请回答1988 旅游 IU 李知恩 李孝利 孝利的名宿 孝利家民宿 IU李智恩 孝利的民宿 李智恩 孝利 民宿 孝利家的民宿"
    #结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__) # 当前文件文件夹所在目录
    color_mask = imread("../img/cloud_back.png") # 读取背景图片
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        # font_path="msyhl.ttc",
        font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=500,
        #最大号字体
        max_font_size=40
    )
    word_cloud = cloud.generate(cut_text) # 产生词云
    word_cloud.to_file("../usertag/"+str(mid)+".jpg") #保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

