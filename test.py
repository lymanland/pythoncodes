from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def selenium_test():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    # browser = webdriver.Chrome()
    try:
        browser.get('https://www.baidu.com')
        input = browser.find_element_by_id('kw')
        input.send_keys('Python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)
    finally:
        browser.close()

#####################################################
from fake_useragent import UserAgent
def ua_test():
    ua = UserAgent()
    
    for i in range(10):
        print(ua.random)
    
import requests
def schedule_test():
    url = 'http://localhost:6800/schedule.json'
    params = {"project":'tutorial',"spider":'quotes'}
    reps = requests.post(url,data=params)
    print(reps.text)

#pip install python-scrapyd-api
from scrapyd_api import ScrapydAPI
def scrapyd_api_test():
    scrapyd = ScrapydAPI('http://localhost:6800')
    print(scrapyd.list_projects())

if __name__ == '__main__':
    # ua_test()
    # schedule_test()
    scrapyd_api_test()
