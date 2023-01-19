from bs4 import BeautifulSoup


# 按照“文件读取三大步”读取保存的网页源代码,记得设置编码格式哦
f = open('science.txt', 'r', encoding='UTF-8')
html = f.read()
f.close()


# 使用BeautifulSoup功能，利用'html.parser'解析器解析html
soup = BeautifulSoup(html, 'html.parser')
print(soup)
# 使用find_all功能查找rel="stylesheet"的 link 的全部标签对象，使用attrs可选参数设置标签属性和值{'rel': 'stylesheet'}
# link_list = soup.find_all('link', attrs={'rel': 'stylesheet'})
# print(link_list)


# 使用find_all功能，查找全部 li 标签
# all_li_tag =

# 使用for循环遍历all_li_tag取值



# 使用select功能,通过 id选择器 搜索class="top" id="banner" 的div标签
# all_li_tag = soup.select('#banner')
# print(all_li_tag)


# 使用select功能,通过 类选择器 搜索 class="news_list"的ul标签
# all_li_tag = soup.select('.news_list')
# print(all_li_tag)


# 使用select功能,通过 标签选择器 搜索li标签,并使用索引[0]取值
# all_li_tag =
# print(all_li_tag)

