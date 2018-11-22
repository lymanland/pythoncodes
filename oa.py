
# -*- coding:utf-8 -*-

import requests
import os
import json

class Spider:

    #页面初始化
    def __init__(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'baitian_oa_user_name=liyijun; baitian_oa_remember_me=WfnpkBahCJK9mUPzr5jcmJWPLGFHVcdL; JSESSIONID=3F2BE5725B8780619BBBD172890C1EFB',
            'Host': 'oa.info',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        self.login_url = 'http://oa.info/login.do'
        self.post_url = 'http://oa.info/login.do'
        self.session = requests.Session()
        self.siteURL = 'http://oa.info/attend/statRecord/getMyMonthRecords.json'


    def writeToJson(self, data):
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
        	
    #获取索引页面的内容
    def getPage(self,year,month):
        url = self.siteURL + "?year=" + str(year) + "&month="+str(month)
        response = self.session.get(url, headers=self.headers)
        # if response.status_code == 200:
        print('getPage response>>')
        print(response.status_code)
        print(response.text)
        resultValues = response.json()['result']['value']
        # for data in resultValues:
        #     print(data['date'], data['workHours'])
        # return response
        return resultValues

    def login(self, password):
        post_data = {
            'userName': 'liyijun',
            'password': password,
            'rememberMe': 'on'
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        print('login response:')
        print(response.status_code)
        # if response.status_code == 200:
        #      print(response.text)

    def run(self, year, month, password='liyijun026'):
        self.login(password)
        resultValues = self.getPage(year,month)
        self.writeToJson(resultValues)
  
spider = Spider()
spider.run(2018,11,'liyijun026')