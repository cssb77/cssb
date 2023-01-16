# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random

se = requests.session()


class Pixiv():

    def __init__(self):
        self.base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.target_url = 'http://www.pixiv.net/search.php?' \
                          'word=%E5%9B%9B%E6%9C%88%E3%81%AF%E5%90%9B%E3%81%AE%E5%98%98&order=date_d&p='
        self.main_url = 'http://www.pixiv.net'
        # headers只要这两个就可以了,之前加了太多其他的反而爬不上
        self.headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.pixiv_id = 'user_avza3787'
        self.password = 'Ji055822'
        self.post_key = []
        self.return_to = 'http://www.pixiv.net/'
        self.load_path = 'E:\新建文件夹 (8)'
        self.ip_list = []

    def login(self):
        post_key_html = se.get(self.base_url, headers=self.headers).text
        post_key_soup = BeautifulSoup(post_key_html, 'lxml')
        self.post_key = post_key_soup.find('input')['value']
        # 上面是去捕获postkey
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'return_to': self.return_to,
            'post_key': self.post_key
        }
        se.post(self.login_url, data=data, headers=self.headers)

    def get_proxy(self):
        html = requests.get('http://haoip.cc/tiqu.htm')
        ip_list_temp = re.findall(r'r/>(.*?)<b', html.text, re.S)
        for ip in ip_list_temp:
            i = re.sub('\n', '', ip)
            self.ip_list.append(i.strip())
            print(i.strip())

    #会被反爬,改成使用
     #   def get_tml(self, url):
      #      response = se.get(url, headers=self.headers)
       #     return response

    def get_html(self, url, timeout, proxy=None, num_entries=5):
        if proxy is None:
            try:
                return se.get(url, headers=self.headers, timeout=timeout)
            except:
                if num_entries > 0:
                    print('获取网页出错,5秒后将会重新获取倒数第', num_entries, '次')
                    time.sleep(5)
                    return self.get_html(url, timeout, num_entries = num_entries - 1)
                else:
                    print('开始使用代理')
                    time.sleep(5)
                    ip = ''.join(str(random.choice(self.ip_list))).strip()
                    now_proxy = {'http': ip}
                    return self.get_html(url, timeout, proxy = now_proxy)
        else:
            try:
                return se.get(url, headers=self.headers, proxies=proxy, timeout=timeout)
            except:
                if num_entries > 0:
                    print('正在更换代理,5秒后将会重新获取第', num_entries, '次')
                    time.sleep(5)
                    ip = ''.join(str(random.choice(self.ip_list))).strip()
                    now_proxy = {'http': ip}
                    return self.get_html(url, timeout, proxy = now_proxy, num_entries = num_entries - 1)
                else:
                    print('使用代理失败,取消使用代理')
                    return self.get_html(url, timeout)

    def get_img(self, html, page_num):
        li_soup = BeautifulSoup(html, 'lxml')  # 传入第page_num页的html
        li_list = li_soup.find_all('li', attrs={'class', 'image-item'})   # 找到li所在位置
        # print('get_list succeed')
        # print(li_list)
        for li in li_list:
            href = li.find('a')['href']  # 直接提取第一个href
            # print('get_href succeed')
            # print(href)
            jump_to_url = self.main_url + href  # 跳转到目标的url
            # print('get_jump_to_url succeed')
            jump_to_html = self.get_html(jump_to_url, 3).text  # 获取图片的html
            # print('get_jump_to_html succeed')

            img_soup = BeautifulSoup(jump_to_html, 'lxml')
            img_info = img_soup.find('div', attrs={'class', 'works_display'})\
                .find('div', attrs={'class', '_layout-thumbnail ui-modal-trigger'})
            # 找到目标位置的信息
            if img_info is None:  # 有些找不到url,如果不continue会报错
                continue
            self.download_img(img_info, jump_to_url, page_num)  # 去下载这个图片

    def download_img(self, img_info, href, page_num):
        title = img_info.find('img')['alt']  # 提取标题
        src = img_info.find('img')['src']  # 提取图片位置
        src_headers = self.headers
        src_headers['Referer'] = href  # 增加一个referer,否则会403,referer就像上面登陆一样找
        try:
            html = requests.get(src, headers=src_headers)
            img = html.content
        except:  # 有时候会发生错误导致不能获取图片.直接跳过这张图吧
            print('获取该图片失败')
            return False

        title = title.replace('?', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('|', '_')\
            .replace('>', '_').replace('<', '_').replace(':', '_').replace('"', '_').strip()
        # 去掉那些不能在文件名里面的.记得加上strip()去掉换行

        if os.path.exists(os.path.join(self.load_path, str(page_num), title + '.jpg')):
            for i in range(1, 100):
                if not os.path.exists(os.path.join(self.load_path, str(page_num), title + str(i) + '.jpg')):
                    title = title + str(i)
                    break
        # 如果重名了,就加上一个数字
        print('正在保存名字为: ' + title + ' 的图片')
        with open(title + '.jpg', 'ab') as f:  # 图片要用b
            f.write(img)
        print('保存该图片完毕')

    def mkdir(self, path):
        path = path.strip()
        is_exist = os.path.exists(os.path.join(self.load_path, path))
        if not is_exist:
            print('创建一个名字为 ' + path + ' 的文件夹')
            os.makedirs(os.path.join(self.load_path, path))
            os.chdir(os.path.join(self.load_path, path))
            return True
        else:
            print('名字为 ' + path + ' 的文件夹已经存在')
            os.chdir(os.path.join(self.load_path, path))
            return False

    def work(self):
        self.login()
        for page_num in range(1, 51):  # 太多页了,只跑50页
            path = str(page_num)  # 每一页就开一个文件夹
            self.mkdir(path)  # 创建文件夹
            # print(self.target_url + str(page_num))
            now_html = self.get_html(self.target_url + str(page_num), 3)  # 获取页码
            self.get_img(now_html.text, page_num)  # 获取图片
            print('第 {page} 页保存完毕'.format(page=page_num))
            time.sleep(2)  # 防止太快被反


pixiv = Pixiv()
pixiv.work()