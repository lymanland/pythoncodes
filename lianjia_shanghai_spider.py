from fake_useragent import UserAgent
from lxml import etree
from bs4 import BeautifulSoup
import pandas as pd
import requests


class LianJianSpider(object):

    def __init__(self):
        self.ua = UserAgent()
        self.headers = {"User-Agent": self.ua.random}
        self.datas = list()

    def get_max_page(self, url):
        reponse = requests.get(url, headers=self.headers)
        if reponse.status_code == 200:
            source = reponse.text
            soup = BeautifulSoup(source, 'html.parser')
            a = soup.find_all("div", class_="page-box house-lst-page-box")
            max_page = eval(a[0].attrs["page-data"])["totalPage"]
            return max_page

        else:
            print("请求失败 statue: {}".format(reponse.status_code))
            return None

    def pares_page(self, url):
        max_page = self.get_max_page(url)
        for i in range(1, max_page + 1):
            url = 'https://sh.lianjia.com/zufang/pa{}/'.format(i)
            print("当前正在爬取: {}".format(url))
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            a = soup.find_all("div", class_="info-panel")
            for j in range(len(a)):
                try:
                    link = a[j].find("a")["href"]
                    print(link)
                    detail = self.parse_detail(link)
                    self.datas.append(detail)
                except:
                    print('get page link is fail')
                    continue
        print("所有数据爬取完成，正在存储到 csv 文件中")
        data = pd.DataFrame(self.datas)
        data.to_csv("链家网租房数据.csv", encoding='utf_8_sig')

    def parse_detail(self, url):
        detail = {}
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            b = soup.find("div", class_="content zf-content")
            detail["月租金"] = int(b.find("span", class_="total").text.strip())
            detail["面积"] = b.find_all("p", class_="lf")[0].text[3:].strip()
            detail["房屋户型"] = b.find_all("p", class_="lf")[1].text[5:].strip()
            detail["楼层"] = b.find_all("p", class_="lf")[2].text[3:].strip()
            detail["房屋朝向"] = b.find_all("p", class_="lf")[3].text[5:].strip()
            detail["地铁"] = b.find_all("p")[4].text[3:].strip()
            detail["小区"] = b.find_all("p")[5].text[3:].split('-')[0].strip()
            detail["位置"] = b.find_all("p")[6].text[3:].strip()
            return detail
        else:
            print("请求失败 statue: {}".format(reponse.status_code))
            return None



class LianJianSpiderThread():

    def __init__(self, url):
        self.ua = UserAgent()
        self.headers = {"User-Agent": self.ua.random}
        self.datas = list()
        self.url = url

    async def get(self, url):
        session = aiohttp.ClientSession()
        reponse = await session.get(url, headers=self.headers)
        result = await reponse.text()
        session.close()
        return result

    def get_max_page(self, url):
        reponse = self.get(url)
        print(reponse)
        soup = BeautifulSoup(reponse, 'html.parser')
        a = soup.find_all("div", class_="page-box house-lst-page-box")
        max_page = eval(a[0].attrs["page-data"])["totalPage"]
        return max_page


    async def pares_page(self, url):
        max_page = self.get_max_page(url)
        for i in range(1, max_page + 1):
            url = 'https://sh.lianjia.com/zufang/pa{}/'.format(i)
            print("当前正在爬取: {}".format(url))
            response = await self.get(url)
            soup = BeautifulSoup(response, 'html.parser')
            a = soup.find_all("div", class_="info-panel")
            for j in range(len(a)):
                try:
                    link = a[j].find("a")["href"]
                    print(link)
                    detail = await self.parse_detail(link)
                    self.datas.append(detail)
                except:
                    print('get page link is fail')
                    continue
        print("所有数据爬取完成，正在存储到 csv 文件中")
        data = pd.DataFrame(self.datas)
        data.to_csv("链家网租房数据.csv", encoding='utf_8_sig')

    async def parse_detail(self, url):
        detail = {}
        response = await self.get(url)
        soup = BeautifulSoup(response, "html.parser")
        b = soup.find("div", class_="content zf-content")
        detail["月租金"] = int(b.find("span", class_="total").text.strip())
        detail["面积"] = b.find_all("p", class_="lf")[0].text[3:].strip()
        detail["房屋户型"] = b.find_all("p", class_="lf")[1].text[5:].strip()
        detail["楼层"] = b.find_all("p", class_="lf")[2].text[3:].strip()
        detail["房屋朝向"] = b.find_all("p", class_="lf")[3].text[5:].strip()
        detail["地铁"] = b.find_all("p")[4].text[3:].strip()
        detail["小区"] = b.find_all("p")[5].text[3:].split('-')[0].strip()
        detail["位置"] = b.find_all("p")[6].text[3:].strip()
        return detail

    def run(self):
        tasks = [asyncio.ensure_future(self.pares_page(self.url))]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

if __name__ == '__main__':
    url = "https://sh.lianjia.com/zufang/"
    spider = LianJianSpiderThread(url)
    spider.run()
    # spider.pares_page(url)
