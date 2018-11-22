from pyecharts import Bar
import pandas as pd
import numpy as np
import pymongo

def drawShopName(db):
    table = db.products
    df = pd.DataFrame(list(table.find()))
    shop_message = df[df.shop_property == '自营'].groupby(['shop_name'])
    shop_com = shop_message['shop_name'].agg(['count'])
    shop_com.reset_index(inplace=True)
    shop_com_last = shop_com.sort_values('count', ascending=False)[:12]
    attr = np.array(shop_com_last['shop_name'])
    v1 = np.array(shop_com_last['count'])
    print('----------shopname----------')
    print('attr>>',attr)
    print('v1>>',v1)
    attr = ["{}".format(i.replace('京东', '').replace('旗舰店', '').replace('自营', '').replace('官方', '').replace('京东', '').replace('电脑', '').replace('产品专营店', '').replace('工作站', '').replace('笔记本', '')) for i in attr]
    v1 = ["{}".format(i) for i in v1]
    print('attr>>',attr)
    print('v1>>',v1)
    # bar = Bar("京东自营商店笔记本种类排行", title_pos='center', title_top='18', width=800, height=400)
    # bar.add("商家", attr, v1, is_convert=True, xaxis_min=10, yaxis_label_textsize=12, is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right', is_yaxis_inverse=True, is_splitline_show=False)
    # bar.render("京东自营商店笔记本种类排行.html")


def drawPrice(db):
    table = db.products
    df = pd.DataFrame(list(table.find()))
    price_info = df['price']
    bins = [0, 2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000, 14000, 16000, 19000, 200000]
    level = ['0-2000', '2000-2500', '2500-3000', '3000-3500', '3500-4000', '4000-5000', '5000-6000', '6000-7000', '7000-8000', '8000-9000', '9000-10000', '10000-12000', '12000-14000', '14000-16000', '16000-19000', '19000以上']
    price_stage = pd.cut(price_info, bins=bins, labels=level).value_counts().sort_index()
    attr = price_stage.index
    v1 = price_stage.values
    print('----------price----------')
    print('attr>>\n',attr)
    print('v1>>\n',v1)
    # bar = Bar('笔记本价格分布柱状图',  title_pos='center', title_top='10', width=800, height=400)
    # bar.add('', attr, v1, is_stack=True, xaxis_rotate=30, yaxis_min=0, xaxis_interval=0, is_splitline_show=False, is_label_show=True)
    # bar.render('笔记本价格分布柱状图.html')


from pyecharts import Pie

def drawCount(db):
    table = db.products
    df = pd.DataFrame(list(table.find()))
    shop_message = df.groupby(['shop_property'])
    shop_com = shop_message['shop_property'].agg({'count':np.size})
    print('shop_com>>\n',shop_com)
    shop_com = shop_message['shop_property'].agg(['count'])
    print('shop_com>>\n',shop_com)
    shop_com.reset_index(inplace=True)
    shop_com_last = shop_com.sort_values('count', ascending=False)
    attr = shop_com_last['shop_property']
    v1 = shop_com_last['count']
    print('----------cont----------')
    print('attr>>\n',attr)
    print('v1>>\n',v1)
    # pie = Pie('商店性质', title_pos='center', width=800, height=400)
    # pie.add('', attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True, legend_orient='vertical', legend_pos='left')
    # pie.render('商店性质.html')


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import jieba
import re

def drawCloud(db):
    table = db.products
    data = pd.DataFrame(list(table.find()))
    data = data[['_id']]

    text = ''
    for line in data['_id']:
        r = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        line = re.sub(r, '', line.replace('笔记本电脑', '').replace('英寸', ''))
        text += ' '.join(jieba.cut(line, cut_all=False))
    # backgroud_Image = plt.imread('computer.jpeg')
    print('text>>',text)
    wc = WordCloud(
        background_color='white',
        # mask=backgroud_Image,
        # font_path='DroidSansMono.ttf',#没有字体，图片是方框乱码
        max_words=2000,
        stopwords=STOPWORDS,
        max_font_size=130,
        random_state=30
    )
    wc.generate_from_text(text)
    # img_colors = ImageColorGenerator(backgroud_Image)
    # wc.recolor(color_func=img_colors)

    plt.imshow(wc)
    plt.axis('off')
    wc.to_file("computer.jpg")
    print("生成词云成功")

if __name__ == "__main__":
    client = pymongo.MongoClient('localhost', 27017)
    db = client.JD_products

    drawShopName(db)
    drawPrice(db)
    drawCount(db)
    # drawCloud(db)