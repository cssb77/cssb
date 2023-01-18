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


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


#if __name__ == '__main__':
#	chaojiying = Chaojiying_Client('18255050535', 'qwerty123456', '924287')	#用户中心>>软件ID 生成一个替换 96001
#	im = open('a.jpg', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
#	print (chaojiying.PostPic(im, 1902))

web = Chrome()

web.get('https://www.chaojiying.com/user/login/')
time.sleep(5)

img = web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/div/img[1]').screenshot_as_png

chaojiying = Chaojiying_Client('18255050535', 'qwerty123456', '924287')									#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
dic = chaojiying.PostPic(img, 1902)
verift_code = dic['pic_str']
print(verift_code)
time.sleep(5)
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys("18255050535")
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys('qwerty123456')
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(verift_code)
time.sleep(10)
web.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()
