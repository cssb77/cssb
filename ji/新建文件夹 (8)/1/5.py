import requests
import json
import re
if __name__ == '__main__':
    url='https://www.qiushibaike.com/text/'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'
    }
    page_text = requests.get(url=url, headers=headers).text
    ex = '<div class="content">.*?<span>'"(.*?)"'</span>.*?</div>'
    list = re.findall(ex, page_text,re.S)
    for i in list:
        i = i.replace('<br/>', '')
        i = i.replace('\n', '')
        print(i+'\n')
