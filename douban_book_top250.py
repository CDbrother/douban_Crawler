"""
目前就到此为止了吧，时间不多了（8月5号晚），还有其他事要忙
使用了requests和etree，urllib和BeautifulSoup还没用
不会使用**正则表达式**将爬取的内容筛选，学会后可以尝试提取电影种类、上映时间
还有可以尝试通过打开电影的链接获取更完整的信息，如演员列表
"""

import requests
from lxml.html import etree  # 新版lxml中如果要使用etree，需要使用lxml.html
import pandas as pd  # csv文件用

number_lists = []
title_lists = []
link_lists = []
score_lists = []
info_lists = []
quote_lists = []


def getpage(page):
    url = 'https://book.douban.com/top250?start={}'.format((page - 1) * 25)  # format函数实现翻页
    # header在F12中的Network中，再刷新一下可以找到
    header = {
        'User-Agent': "Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/75.0.3770.142Safari/537.36"}
    req = requests.get(url, headers=header)  # 获取URL
    # print(req.text)  # 看网页源码
    return req.text


def parse(text):  # 解析数据
    html = etree.HTML(text)  # 初始化&标准化
    # xpath()返回**列表**
    # 一开始不知道是列表，又append到另一个列表里，导致有两层中括号，for循环只能算一个，使用replace会导致无法识别列表，只能算str
    # 因为源码含有多个div和span，需要标注序号；部分需要text()，否则会报错
    contents_title = html.xpath('//td[2]/div[1]/a/@title')
    contents_url = html.xpath('//td[2]/div[1]/a/@href')
    contents_score = html.xpath('//td[2]/div[2]/span[2]/text()')
    contents_info = html.xpath('//td[2]//p[1]/text()')  # 日期也是有\xa0/\xa0出现，目前无法解决
    contents_quote = html.xpath('//td[2]//p[2]/span/text()')
    print(contents_quote)
    # contents_txt = zip(contents_title, contents_url, contents_score, contents_info, contents_quote) # 好几本书都没有quote
    contents_txt = zip(contents_title, contents_url, contents_score, contents_info)
    # zip()函数，contents=[(contents_title,contents_url， contents_score),()...]，是元组
    return contents_txt, contents_title, contents_url, contents_score, contents_info, contents_quote


def write(data):
    raw_contents = getpage(data)  # 此处我遇到了一个问题：序号特别多，结果发现内容使用的是没有parse过的数据😓
    contents, titles, urls, scores, info, quote = parse(raw_contents)
    title_lists.extend(titles)  # 将多个网页的内容拼接到一个列表
    link_lists.extend(urls)
    score_lists.extend(scores)
    info_lists.extend(info)
    quote_lists.extend(quote)
    print(len(title_lists))
    print(len(link_lists))
    print(len(score_lists))
    print(len(info_lists))
    print(len(quote_lists))
    a = 0
    # 方法一(txt)：
    with open('douban_book_top250(txt).txt', 'a', encoding='utf-8') as f:
        for content_tuple in contents:
            f.write("No " + str((i - 1) * 25 + a + 1) + ":\t")  # 序号
            a += 1
            # 不会正则表达式，不会分割，对\xa0/\xa0出现等问题使用比较原始的replace函数
            content1 = str(content_tuple).replace('(', '')
            content2 = content1.replace(')', '')
            content3 = content2.replace('\'', '')
            content4 = content3.replace(',', ' ')
            content5 = content4.replace('\\xa0', '')
            content6 = content5.replace('/', '', 1)
            content7 = content6.replace('\\n                            ', '')
            content8 = content7.replace("\\n", '')
            f.write(content8.strip() + '\n')


for i in range(1, 10):
    write(i)
    print(f"正在爬取第{i}页")

# 方法二(csv)：
b = 0
for x in range(len(title_lists)):
    number_lists.append(b + 1)
    b += 1
# contents_info = {'number': number_lists, 'name': title_lists, 'link': link_lists, 'score': score_lists}
contents_info = {'number': number_lists, 'name': title_lists, 'link': link_lists,
                 'score': score_lists, 'info': info_lists}
# contents_info = {'number': number_lists, 'name': title_lists, 'link': link_lists,
#                  'score': score_lists, 'info': info_lists, 'quote': quote_lists}
# 好几本书都没有quote，也不清楚有什么办法快速加空值，先这样吧
print(contents_info)
frame = pd.DataFrame(contents_info)  # csv文件
frame.to_csv(r'D:\programme_study\Python_work\crawler\douban_book_top250(csv).csv')  # 乱码的话，记事本打开，转码ANSI
print(frame)
