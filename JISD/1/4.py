import requests
import re
import os
if __name__ == '__main__':
    if not os.path.exists('./1'):
        os.mkdir('./1')
    url = 'https://www.qiushibaike.com/imgrank/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'
    }
    page_text = requests.get(url=url,headers=headers).text
    ex = '<div class="thumb">.*?<img src="(.*?)" alt.*?</div>'
    img_src_list = re.findall(ex,page_text,re.S)
    for src in img_src_list:
        print('OK')
        src = 'https:'+ src
        url = src
        img_data = requests.get(url=url,headers=headers).content
        img_name = src.split('/')[-1]
        imgPath = './1/'+img_name
        print('OK')
        with open(imgPath,'wb') as fp:
            fp.write(img_data)
            print('OK')

    input('OK')