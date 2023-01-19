import requests
import json


if __name__ == '__main__':
    url='https://movie.douban.com/j/chart/top_list'
    word = input('enter a word:')
    ee = input('ee:')
    param ={
        'type': '24',
        'interval_id': '100:90',
        'action':'',
        'start': word,
        'limit': ee,
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'
    }
    response = requests.get(url=url,params=param,headers=headers)
    list_data = response.json()
    for i in list_data:
        print(i['title'])
    input('OK')