import scrapy
from selenium import webdriver
import time
from PIL import Image

class WeiboSpider(scrapy.Spider):
name = 'weibo'
allowed_domains = ['https://weibo.com/']
start_urls = ['https://weibo.com/']

def parse(self, response):
browser = webdriver.Chrome(executable_path="C:/Users/Mr JIE/Chromedriver2.33/chromedriver.exe")
browser.get('https://weibo.com')
time.sleep(15)
browser.maximize_window()
browser.find_elements_by_class_name("W_input")[1].send_keys("")#账号
time.sleep(3)
browser.find_elements_by_class_name("W_input")[2].send_keys("")#密码
time.sleep(3)
# 手动截图处理验证码
browser.get_screenshot_as_file('yzm.png')
yzm = Image.open('yzm.png')
# 这里屏幕纵坐标值都要减105才等于真实值
left = 1332
top = 228
right = 1460
bottom = 276
yzm = yzm.crop((left,top,right,bottom))#两个括号没错
yzm.save('yzm.png')
from ArticleSpider.common import chaojiying
a = chaojiying.Chaojiying_Client('1825505035','qwerty123456','924287')#填写用户名,填写密码,填写软件id
im = open('ypg.png', 'rb').read()#图片的路径
code = a.PostPic(im, 1902)
browser.find_elements_by_class_name("W_input")[3].send_keys(code['pic_str'])
time.sleep(3)
browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
time.sleep(3000)
pass