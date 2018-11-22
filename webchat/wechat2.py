import itchat
import os
import random
from PIL import Image
import math
import re
import matplotlib.pyplot as plt
import io
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import numpy as np


def draw(datas):
    for key in datas.keys():
        plt.bar(key, datas[key])

    plt.legend()
    plt.xlabel('sex')
    plt.ylabel('rate')
    plt.title("Gender of Alfred's friends")
    plt.show()

def parse_friedns(itchat_friedns):
    text = dict()
    friedns = itchat_friedns[0:]
    print('parse_friedns>>>>>')
    print(friedns)
    male = "male"
    female = "female"
    other = "other"
    for i in friedns[1:]:
        sex = i['Sex']
        if sex == 1:
            text[male] = text.get(male, 0) + 1
        elif sex == 2:
            text[female] = text.get(female, 0) + 1
        else:
            text[other] = text.get(other, 0) + 1
    total = len(friedns[1:])
    print("男性好友： %.2f%%" % (float(text[male]) / total * 100) + "\n" +
          "女性好友： %.2f%%" % (float(text[female]) / total * 100) + "\n" +

          "不明性别好友： %.2f%%" % (float(text[other]) / total * 100))
    draw(text)

"""
获取好友头像、签名和性别
"""
def get_friend():
    # 登录微信
    itchat.auto_login(True)
    # 获取微信所有的好友对象
    friends = itchat.get_friends(update=True)
    parse_friedns(friends)
    # 获取当前路径 创建pic文件
    pic_path = os.getcwd() + '\\pic\\'
    # 文件夹不存在 则创建
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)

    file = open('Signature.txt', 'a+', encoding='utf-8')
    # 性别字典
    sex_arr = {}

    x = 0
    for i, friend in enumerate(friends):
        # 性别
        sex = friend['Sex']
        if sex == 1:
            sex_arr['Boy'] = sex_arr.get('Boy', 0) + 1
        elif sex == 2:
            sex_arr['Girl'] = sex_arr.get('Girl', 0) + 1
        else:
            sex_arr['Unknow'] = sex_arr.get('Unknow', 0) + 1

        # 替换掉个性签名中的表情等字符..span, emoji
        signature = friend['Signature'].strip().replace('span', '').replace('emoji', '').replace('class', '')
        rec = re.compile('[^\u4e00-\u9fa5^]')
        signature = rec.sub("", signature)
        # 个性签名写入文件
        file.write(signature + "\n")
        # 通过userName 获取头像byte
        img_byte = itchat.get_head_img(userName=friend['UserName'])
        uuserName = friend['UserName'].strip().replace('span', '').replace('emoji', '').replace('class', '')
        # img = open(pic_path + str(rec.sub("", uuserName)) + '.jpg', 'wb')
        img = open(pic_path + str(x) + '.jpg', 'wb')
        # 图片写入pic文件夹
        print('签名',signature)
        # print(friend['UserName'], uuserName)
        img.write(img_byte)
        img.close()
        x += 1
        print('img write end>>>>>>>')
        # try:
        #    img.write(img_byte)
        # except OSError as e:
        #     print('OSError:', e)
        # else:
        #     print('noerro:')
        # finally:
        #     img.write(img_byte)
        #     img.close()
        
    return sex_arr

"""
 创建图片
"""
def get_image():
    x = 0
    y = 0
    # 获取pic下 图像列表
    imgs = os.listdir("pic")
    print('imgs>>')
    print(imgs)
    random.shuffle(imgs)
    # 创建640*640的图片用于填充各小图片
    newImg = Image.new('RGBA', (1024, 1024))
    # 以640*640来拼接图片，math.sqrt()开平方根计算每张小图片的宽高，
    width = int(math.sqrt(1024 * 1024 / len(imgs)))
    # 每行图片数
    numLine = int(1024 / width)

    for i in imgs:
        if not i.endswith('jpg'):
            continue
        print('拼接图片》》')
        print(i)
        pic_path = os.getcwd() + '\\pic\\'
        # img = Image.open("pic/" + i)
        try:
            img = Image.open(pic_path + i)
            # print('try...')
        except OSError as e:
            print('OSError:', i)
        else:
            # print('no error!')
            # 缩小图片
            img = img.resize((width, width), Image.ANTIALIAS)
            # 拼接图片，一行排满，换行拼接
            newImg.paste(img, (x * width, y * width))
            x += 1
            if x >= numLine:
                x = 0
                y += 1
        # finally:
        #     print('finally...')
    newImg.save("all.png")

"""
词云
"""
def create_cloud():
    path = os.getcwd() + '/signature.txt'
    # 读signature.txt文本内容
    content = open(path, encoding='utf-8').read()
    print('content>>>>>>>>')
    print(content)
    # 词云配置
    wc = WordCloud(
        # 背景色
        background_color='white',
        # 最大显示的词数
        max_words=1000,
        height=500,
        width=500,
        # worldcloud 本身不支持中文，需要指定字体文件路径
        font_path='DroidSansFallbackFull.ttf',
        max_font_size=60,
        # 随机配色方案数
        random_state=30
    ).generate(content)
    # ).fit_words(content)

    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    wc.to_file('signature_cloud.png')

if __name__ == '__main__':
    get_friend()
    get_image()
    create_cloud()