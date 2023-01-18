import requests


def get_html_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r.encoding = 'UTF-8'
        return r.text
    else:
        return '爬取失败！'


url = 'https://show.ybccode.com/news_l5/science/'
html = get_html_text(url)
# 写入文件操作
# 将网页源代码按照“文件写入三大步”写入文件保存，记得设置编码格式哦
f = open()
f.write()
f.close()
