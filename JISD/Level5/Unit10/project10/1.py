from bs4 import BeautifulSoup


# 读取保存的网页源代码
f = open('science.txt', 'r', encoding='UTF-8')
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
    pass
    # 使用find功能,查找li标签对象中的img标签对象
    # news_image =

    # 使用get功能,获取img标签对象(news_image)的src属性，取出链接
    # news_image_link =

    # 使用find功能,查找li标签对象中的a标签对象
    # news =

    # 使用get功能,获取a标签对象(news)的href属性，取出链接
    # news_link =
    # 使用get_text功能,获取a标签对象(news)内的文本信息
    # news_name =

    # 使用find_all功能,查找li标签对象中的全部span标签对象
    # span_list =

    # 使用get_text功能,获取span标签对象(span_list)内的文本信息，并使用索引[0]取出“作者”信息
    # news_writer =

    # 使用get_text功能,获取span标签对象(span_list)内的文本信息，并使用索引[1]取出“时间”信息
    # news_time =

    # 将数据存入一维列表 [news_name, news_writer, news_time, news_link, news_image_link]
    # news_item =
    # print(news_item)
