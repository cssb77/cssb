import requests
import re
import os
if __name__ == '__main__':
    url = 'http://127.0.0.1:5001/ji4'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'
    }
    ee = input('ee:')
    h={
        'jie':ee
    }
    r = requests.post(url=url,params=h)
    r.encoding = 'utf-8'
    input('ok')
    input(r.txt)