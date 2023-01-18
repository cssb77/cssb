from hashlib import md5
from selenium.webdriver import Chrome
import time
import requests
from hashlib import md5
import requests
from hashlib import md5
import click



def www():
    web = Chrome()

    web.get('https://show.ybccode.com/ybc_video_l5/login/')
    time.sleep(0)

    web.find_element_by_xpath('/html/body/div/div/form/div[1]/input').send_keys("11114")
    web.find_element_by_xpath('/html/body/div/div/form/div[2]/input').send_keys('123456')
    time.sleep(1)
    #web.find_element_by_xpath('/html/body/div/div/form/div[4]/button').clink()
def qqq():
    web = Chrome()
    while True:
        www()
        web.get('https://show.ybccode.com/ybc_video_l5/login/')
qqq()