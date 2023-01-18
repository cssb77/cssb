import requests
import json
if __name__ == '__main__':
    post_uil='https://fanyi.baidu.com/sug'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'
    }
    word = input('enter a word')
    data={
        'kw':word
    }
    response = requests.post(url=post_uil,data=data,headers=headers)
    dic_odj = response.json()
    print(dic_odj)
    fileName = word+'.json'
    fp = open(fileName,'w',encoding='utf-8')
    json.dump(dic_odj,fp=fp,ensure_ascii=False)
    print('OK')