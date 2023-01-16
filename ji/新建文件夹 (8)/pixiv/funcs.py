import getpass
import json
import os
import pickle
import requests

# hds里的referer非常关键, 没它就没法下载缩略图
hds = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache', 'pragma': 'no-cache',
    'referer': 'https://www.pixiv.net/',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36 '
                  'Edg/89.0.774.68'
}


# 对字符串的每一个字符做异或的加密/解密函数. 娱乐用.
def decode(s: str) -> str:
    s = s[::-1]
    res = ''
    for c in s:
        res += chr(ord(c) ^ 3)
    return res


# 将selenium风格的list形式的cookie转换为requests能用的dict形式.
def sele2req(sele_cookie: list) -> dict:
    d = {}
    for each in sele_cookie:
        d[each['name']] = each['value']
    return d


# 使用requests, 下载作品缩略图的函数.
def download_thumbnail(pixiv_id: str, url: str, pxy: str = ''):
    # 缩略图已存在, 直接跳过.
    if os.path.exists(f'thumbs\\{pixiv_id:d}.jpg'):
        return True
    custom_proxy = {
        'http': pxy,
        'https': pxy,
    }
    r = None
    if pxy:
        for i in range(1, 11):
            try:
                r = requests.get(
                    url, proxies=custom_proxy,
                    headers=hds,
                    timeout=3
                )
                r.raise_for_status()
                break
            except:
                pass
    else:
        for i in range(1, 11):
            try:
                r = requests.get(
                    url,
                    headers=hds,
                    timeout=3
                )
                r.raise_for_status()
                break
            except:
                pass
    if r:
        try:
            with open(f'thumbs\\{pixiv_id:d}.jpg', 'wb') as f:
                f.write(r.content)
        except OSError:
            try:
                os.mkdir('thumbs')
            except OSError:
                print(f'Failed to download thumbnail for {pixiv_id:d}(No response).')
                return False
            with open(f'thumbs\\{pixiv_id:d}.jpg', 'wb') as f:
                f.write(r.content)
        return True
    else:
        print(f'Failed to download thumbnail for {pixiv_id:d}.')
        return False


# 向settings.pck中增添/修改数据.
def config_settings(target_key, target_value):
    temp_dict = {}
    try:
        with open('settings.pck', 'rb') as f:
            temp_dict = pickle.load(f)
    except (FileNotFoundError, EOFError):
        pass
    with open('settings.pck', 'wb') as f:
        temp_dict[target_key] = target_value
        pickle.dump(temp_dict, f)


def user_info_generate():
    filename = 'user_info.json'
    while True:
        username = input('Pixiv account >>>')
        if username:
            break
        else:
            print('ERROR: username must not be empty!')
    while True:
        password = getpass.getpass('Pixiv account password >>>')
        if password:
            break
        else:
            print('ERROR: password must not be empty!')
    proxy = input(
        'Proxy (input nothing and press enter if you do not need one) >>>'
    )
    d = {
        'username': username, 
        'password': password, 
        'height': 20,
        'width': 4,
        'pic_size': 240
    }
    if proxy:
        d['proxy'] = proxy
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(d))
