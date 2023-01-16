import aiohttp
import asyncio
import os
import pickle
import sqlite3
import sys
import time

import msedge.selenium_tools
import requests
import selenium.common.exceptions
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import funcs

WAIT_TIME = 600  # 在登录页面等待10分钟
MAX_NUM = 131072

hds_pc = {
    'referer': 'https://www.pixiv.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44'
}
hds_mobile = {
    'referer': 'https://www.pixiv.net/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 '
                  'Mobile Safari/537.36 Edg/90.0.818.46'
}

# 较为关键, 设置webdriver的加载是阻塞还是不阻塞
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
dc = DesiredCapabilities.EDGE
dc['pageLoadStrategy'] = 'none'


class StoppableThread(threading.Thread):
    def __init__(self, func=None, args=()):
        super().__init__()
        self.func = func
        self.args = args
        self.is_running = True

    def run(self):
        task = threading.Thread(
            target=self.func,
            args=self.args
        )
        task.setDaemon(True)
        task.start()
        while self.is_running and task.is_alive():
            task.join()
            time.sleep(0.5)

    def stop(self):
        self.is_running = False


class PixivLoginPage:
    def __init__(self, opt_proxy: str = ''):
        self.opt = msedge.selenium_tools.EdgeOptions()
        self.opt.use_chromium = True
        self.opt.add_experimental_option(
            'prefs',
            {"profile.managed_default_content_settings.images": 2}
        )
        if opt_proxy:
            self.raw_proxy = opt_proxy
            self.proxy = '--proxy-server={pxy:s}'.format(pxy=opt_proxy)
            self.opt.add_argument(self.proxy)
        # 'eager' strategy can be found in the doc of selenium
        self.opt.page_load_options = 'eager'
        self.driver = None
        self.custom_cookie_list = None
        self.custom_cookie_dict = None

    def login(self, username: str, password: str):
        print('Start login as', username, '...', end='')
        if os.path.exists('cookie.pck'):
            print('cookie.pck Found')
            with open('cookie.pck', 'rb') as f:
                try:
                    temp_cookie = pickle.load(f)[username]
                    expire_time = -1
                    for each in temp_cookie:
                        temp = each.get('expiry', False)
                        if temp:
                            expire_time = max(expire_time, int(temp))
                    if int(time.time()) < expire_time:
                        self.custom_cookie_list = temp_cookie
                        self.custom_cookie_dict = funcs.sele2req(temp_cookie)
                        print('Login success.')
                        return 0
                    print('Cookie expired', file=sys.stderr)
                except Exception as e:
                    print(type(e), e, file=sys.stderr)
        login_url = 'https://accounts.pixiv.net/login'
        self.driver = msedge.selenium_tools.Edge('./msedgedriver.exe', options=self.opt)
        for i in range(1, 6):
            try:
                self.driver.get(login_url)
                WebDriverWait(self.driver, 30).until(
                    ec.presence_of_element_located(
                        (By.XPATH, '//input[@autocomplete="username"]')
                    )
                )
                un_elem = self.driver.find_element_by_xpath(
                    '//input[@autocomplete="username"]')
                pw_elem = self.driver.find_element_by_xpath(
                    '//input[@autocomplete="current-password"]')
                un_elem.clear()
                un_elem.send_keys(username)
                pw_elem.clear()
                pw_elem.send_keys(password)
                # Start to login
                un_elem.send_keys(Keys.RETURN)
                # WebDriverWait(self.driver, WAIT_TIME).until(
                #     ec.presence_of_element_located(
                #         (By.XPATH, r'''//div[@id="root"]''')
                #     )
                # )
                WebDriverWait(self.driver, WAIT_TIME).until(
                    ec.title_is('pixiv')
                )
                break
            except selenium.common.exceptions.TimeoutException:
                print(f'Retrying login...{i:d}...')
        # useful when reusing our identity
        temp_cookie = {
            username: self.driver.get_cookies()
        }
        with open('cookie.pck', 'wb') as f:
            pickle.dump(temp_cookie, f)
        self.custom_cookie_list = temp_cookie
        self.custom_cookie_dict = funcs.sele2req(temp_cookie[username])
        self.driver.quit()
        print('Login success.')


class PixivMobileArtPage:
    def __init__(self, pixiv_id):
        self.url = f'https://www.pixiv.net/touch/ajax/illust/details?' \
                   f'illust_id={pixiv_id:s}&lang=zh'
        self.custom_proxy = None
        self.custom_cookies = None
        self.session = None
        self.like_num = -1
        self.is_R18 = False

    def set_proxy(self, new_proxy):
        if new_proxy:
            self.custom_proxy = {
                'http': new_proxy,
                'https': new_proxy
            }

    def set_cookies(self, new_cookies):
        self.custom_cookies = new_cookies

    def set_session(self, new_session):
        self.session = new_session

    def parse(self):
        try:
            for i in range(5):
                r = self.session.get(
                    self.url, headers=hds_mobile, timeout=10,
                    cookies=self.custom_cookies,
                    proxies=self.custom_proxy
                )
                r.raise_for_status()
                data_in_json = r.json()
                try:
                    data_in_json = data_in_json['body']['illust_details']
                except KeyError:
                    continue
                tags = data_in_json['tags']
                if 'R-18' in tags or 'R-18G' in tags:
                    self.is_R18 = True
                self.like_num = int(data_in_json['bookmark_user_total'])
                break
        except Exception as e:
            print(type(e), e)


class PixivMobilePage:
    def __init__(self):
        self.cc = 0

        self.session = requests.Session()
        self.raw_proxy = None
        self.custom_proxy = None
        self.search_keyword = None
        self.custom_cookies = None
        self.current_page = 0
        self.total_page = 0
        self.total_num = 0
        self.year = time.localtime(time.time()).tm_year
        self.is_first_half_year = False
        self.lowest_like = 150
        # order=date scd=2020-09-03 ecd=2021-09-03
        self.url = 'https://www.pixiv.net/ajax/search/artworks/{1:s}?' \
                   'word={1:s}&order=date_d&mode=all&p={0:d}&s_mode=s_tag_full&' \
                   'type=all&lang=zh&scd={2:4d}-07-01&ecd={2:4d}-12-31', \
                   'https://www.pixiv.net/ajax/search/artworks/{1:s}?' \
                   'word={1:s}&order=date_d&mode=all&p={0:d}&s_mode=s_tag_full&' \
                   'type=all&lang=zh&scd={2:4d}-01-01&ecd={2:4d}-06-30'
        # self.url = 'https://www.pixiv.net/touch/ajax/search/illusts?' \
        #            'include_meta=0&p={0:d}&type=all&word={1:s}' \
        #            '&s_mode=s_tag_full&lang=zh' \
        #            '&scd={2:4d}-01-01&ecd={2:4d}-06-30', \
        #            'https://www.pixiv.net/touch/ajax/search/illusts?' \
        #            'include_meta=0&p={0:d}&type=all&word={1:s}' \
        #            '&s_mode=s_tag_full&lang=zh' \
        #            '&scd={2:4d}-07-01&ecd={2:4d}-12-31'
        self.search_thread = None
        self.go_ahead = True

    def set_proxy(self, new_proxy: str):
        if new_proxy:
            self.raw_proxy = new_proxy
            self.custom_proxy = {
                'http': new_proxy,
                'https': new_proxy
            }

    def set_search_keyword(self, new_keyword: str):
        self.search_keyword = new_keyword

    def set_cookies(self, dict_of_cookie: dict):
        self.custom_cookies = dict_of_cookie

    def parse_one_page(self, page=1, refresh=False):
        artworks = []
        for i in range(5):
            try:
                if self.custom_proxy:
                    r = self.session.get(
                        self.url[self.is_first_half_year].format(page, self.search_keyword, self.year),
                        headers=hds_pc, timeout=8,
                        proxies=self.custom_proxy,
                        cookies=self.custom_cookies
                    )
                else:
                    r = self.session.get(
                        self.url[self.is_first_half_year].format(page, self.search_keyword, self.year),
                        headers=hds_pc, timeout=8,
                        cookies=self.custom_cookies
                    )
                r.raise_for_status()
                data_in_json = r.json()
                try:
                    data_in_json = data_in_json['body']['illustManga']
                except KeyError:
                    continue
                works = data_in_json['data']
                work_per_page = len(works)
                if not work_per_page:
                    print(f'work_per_page = {work_per_page}')
                    return []
                self.total_num = int(data_in_json['total'])
                if refresh:
                    if self.total_num % work_per_page:
                        self.total_page = self.total_num // work_per_page + 1
                    else:
                        self.total_page = self.total_num // work_per_page
                self.current_page = page
                t0 = time.time()

                async def temp_task(cs: aiohttp.ClientSession, tu: dict, arts: list):
                    temp_url = f'https://www.pixiv.net/touch/ajax/illust/details?' \
                               f'illust_id={tu["id"]:s}&lang=zh'
                    res_dict = {
                        'pixiv_id': tu['id'],
                        'title': tu['title'],
                        'thumb_url': tu['url'].replace('\\', ''),
                    }
                    # async with aiohttp.ClientSession() as cs:
                    for _ in range(8):
                        try:
                            async with cs.get(
                                url=temp_url, headers=hds_mobile,
                                proxy=self.raw_proxy, timeout=8
                            ) as _r:
                                data_json = await _r.json()
                                try:
                                    data_json = data_json['body']['illust_details']
                                except KeyError:
                                    continue
                                tags = data_json['tags']
                                if 'R-18' in tags or 'R-18G' in tags:
                                    res_dict['is_R18'] = True
                                else:
                                    res_dict['is_R18'] = False
                                res_dict['like_num'] = int(data_json['bookmark_user_total'])
                                arts.append(res_dict)
                                break
                        except asyncio.exceptions.TimeoutError:
                            pass
                        except Exception as _e:
                            print(type(_e), f'Page {page}: {_e.__str__()}', file=sys.stderr)

                async def temp_visit(ws):
                    jobs = []
                    jobs_append = jobs.append
                    async with aiohttp.ClientSession() as cs:
                        for each in ws:
                            jobs_append(temp_task(cs, each, artworks))
                        await asyncio.gather(*jobs)

                loop_now = asyncio.new_event_loop()
                asyncio.set_event_loop(loop_now)
                # tasks = [asyncio.ensure_future(
                #     temp_task(x, artworks)
                # ) for x in works]
                # loop_now.run_until_complete(asyncio.wait(tasks))
                loop_now.run_until_complete(temp_visit(works))
                loop_now.close()

                t1 = time.time()
                funcs.config_settings(
                    self.search_keyword,
                    (self.current_page, self.year, self.is_first_half_year)
                )
                print("%d/%d: %.1fs" % (page, self.total_page, t1 - t0))
                return artworks
            except Exception as e:
                print(type(e), e, 'Retrying to parse page {}...trying {}...'.format(page, i + 1), file=sys.stderr)
        print('Failed to parse page', page, '.')
        return []

    def write_to_storage(self, search_keyword, artworks, lowest_like=150):
        # If not exists, program will create one.
        content = sqlite3.connect('storage.db')
        cur = content.cursor()
        try:
            cur.execute(f'CREATE TABLE [{search_keyword:s}] ('
                        f'    pixiv_id INT NOT NULL UNIQUE PRIMARY KEY,\n'
                        f'    title CHAR(1024) NOT NULL,\n'
                        f'    thumb_url CHAR(2048) NOT NULL,\n'
                        f'    like_num INT, \n'
                        f'    is_R18 INT\n'
                        f')')
            print(
                f'A new table [{search_keyword:s}] has been created...',
                end='', flush=True
            )
        except sqlite3.OperationalError:
            # The table has been created
            pass
        for each in artworks:
            try:
                if each['like_num'] < lowest_like:
                    continue
                t = (
                    each['pixiv_id'],
                    each['title'],
                    each['thumb_url'],
                    each['like_num'],
                    each['is_R18']
                )
                cur.execute(f'INSERT INTO [{search_keyword:s}] VALUES (?, ?, ?, ?, ?)', t)
            except sqlite3.OperationalError:
                print(f'''
                    INSERT INTO {search_keyword} VALUES (
                        \"{each['pixiv_id']}\",
                        \"{each['title']}\",
                        \"{each['thumb_url']}\",
                        \"{each['like_num']}\",
                        \"{each['is_R18']}\"
                )''')
            except sqlite3.IntegrityError:
                # This artwork has been added into the storage
                t = (each['like_num'], each['is_R18'], each['pixiv_id'])
                cur.execute(
                    f'UPDATE [{search_keyword:s}] SET like_num=?, is_R18=? WHERE pixiv_id=?',
                    t
                )
        cur.close()
        content.commit()
        content.close()

    def get_artworks_from_all_pages(self, _from=1, _to=MAX_NUM):
        self.cc = 0

        def temp_func(a, need_refresh=False):
            if not self.go_ahead:
                return False
            # self.current_page = a
            artworks = self.parse_one_page(a, need_refresh)
            if not artworks:
                self.cc += 1
                return False
            # print(f'Parsing page {a}/{self.total_page} Successfully.', flush=True)
            self.write_to_storage(self.search_keyword, artworks, self.lowest_like)
            self.cc = 0
            return True

        while self.go_ahead:
            temp_func(_from, True)
            if self.cc > 4:
                funcs.config_settings(
                    self.search_keyword,
                    (1, time.localtime(time.time()).tm_year, False)
                )
                print(self.year, f'is_first_half = {self.is_first_half_year}', file=sys.stderr)
                break
            # elif not self.total_page:
            #     print('NO PAGE AVAILABLE', file=sys.stderr)
            #     funcs.config_settings(
            #         self.search_keyword,
            #         (1, time.localtime(time.time()).tm_year, False)
            #     )
            #     break
            # elif self.year < 2007:
            #     print('TOO EARLY', file=sys.stderr)
            #     funcs.config_settings(
            #         self.search_keyword,
            #         (1, time.localtime(time.time()).tm_year, False)
            #     )
            #     break
            print(
                f'[{self.search_keyword}] has '
                f'{self.total_num} artworks '
                f'in the {"first" if self.is_first_half_year else "second"} half year '
                f'of {self.year}.')
            _from += 1

            if _to == MAX_NUM:
                _to = self.total_page

            def show_progress(a, b):
                with ThreadPoolExecutor(max_workers=8) as tp:
                    tasks = []
                    task_add = tasks.append
                    while a <= b:
                        task_add(tp.submit(temp_func, a))
                        a += 1

            self.search_thread = StoppableThread(show_progress, (_from, _to))
            self.search_thread.start()
            self.search_thread.join()
            print(
                f'Artworks of [{self.search_keyword}] '
                f'in the {"first" if self.is_first_half_year else "second"} half year '
                f'of {self.year} is ready.')
            self.is_first_half_year = not self.is_first_half_year
            _from = 1
            _to = MAX_NUM
            if not self.is_first_half_year:
                self.year -= 1

    def set_year(self, x=time.localtime(time.time()).tm_year):
        self.year = x
