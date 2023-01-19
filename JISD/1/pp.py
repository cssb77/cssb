#!/usr/bin/env python
# coding:utf-8
import requests
from hashlib import md5
from selenium.webdriver import Chrome
import time
import requests
from hashlib import md5
import requests
from hashlib import md5



i = ['qwerty123456','qwerty1234567','qwertyu1234567']
for q in i:
    print(q)
    web = Chrome()
    web.get('https://mail.qq.com/')


    web.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/form/div[1]/div/input').send_keys("2506325721")
    web.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/form/div[2]/div[1]/input').send_keys(q)
    time.sleep(10)
    web.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/form/div[4]/div/a').clink()
    web.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/form/div[4]/a/input').clink()
