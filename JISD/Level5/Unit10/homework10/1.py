from bs4 import BeautifulSoup


# 选择打开给定的文件(sports.txt)并读取
f = open('sports.txt', 'r', encoding='UTF-8')
html = f.read()
f.close()
# 使用BeautifulSoup功能，利用'html.parser'解析器解析html
soup = BeautifulSoup(html, 'html.parser')
# 使用select功能,通过 类选择器 搜索 class="news_list" 的ul标签,并使用索引[0]取值
all_ul_tag = soup.select('.news_list')[0]
# 使用find_all功能，查找all_ul_tag标签对象中的全部 li 标签对象
all_li_tag = all_ul_tag.find_all('li')
# 使用for循环遍历all_li_tag标签对象
for li in all_li_tag:
    # 使用find功能,查找li标签对象中的img标签对象
    news_image = li.find('img')
    # 使用get功能,获取img标签对象(news_image)的src属性，取出链接
    news_image_link = news_image.get('src')
    # 【提示1】使用find功能,查找li标签对象中的a标签对象
    news = li.find('a')
    # 【提示2】使用get功能,获取a标签对象(news)的href属性，取出链接
    news_link =news.get('href')
    # 【提示3】使用get_text功能,获取a标签对象(news)内的文本信息
    news_name =news.get_text()
    # 【提示4】使用find_all功能,查找li标签对象中的全部span标签对象
    span_list =li.find_all('span')
    # 使用get_text功能,获取span标签对象(span_list)内的文本信息，并使用索引[0]取出“作者”信息
    news_writer = span_list[0].get_text()
    # 使用get_text功能,获取span标签对象(span_list)内的文本信息，并使用索引[1]取出“时间”信息
    news_time = span_list[1].get_text()
    # 将数据存入一维列表 [news_name, news_writer, news_time, news_link, news_image_link]
    news_item = [news_name, news_writer,
                 news_time, news_link, news_image_link]
    print(news_item)
