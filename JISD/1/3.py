import requests
if __name__ == '__main__':
    url = 'https://tse1-mm.cn.bing.net/th/id/R-C.a897fe6a5e74512ba7e2dc00e96df58a?rik=JpKKI07PLothvg&riu=http%3a%2f%2fmash.org.au%2fwp-content%2fuploads%2f2017%2f12%2f88-sales.jpeg&ehk=bcrBzsz3TyaJHolbF%2bkGU9qWOnZh3c5DjKwrcnyjRsI%3d&risl=&pid=ImgRaw&r=0'
    img_data=requests.get(url=url).content
    with open('./1/1.jpg','wb') as fp:
        fp.write(img_data)