"""
目前就到此为止了吧，时间不多了（8月6号晚），还有其他事要忙
使用了requests和etree，urllib和BeautifulSoup还没用
不会使用**正则表达式**将爬取的内容筛选，学会后可以尝试提取电影种类、上映时间
还有可以尝试通过打开电影的链接获取更完整的信息，如演员列表
"""

import requests
# from bs4 import BeautifulSoup   # 此文件弃用BeautifulSoup
from lxml.html import etree  # 新版lxml中如果要使用etree，需要使用lxml.html
import pandas as pd  # csv文件用

number_lists = []
title_lists = []
title_origin_lists = []
link_lists = []
score_lists = []
staff_lists = []
other_lists = []
quote_lists = []


def getpage(page):
    url = 'https://movie.douban.com/top250?start={}'.format((page - 1) * 25)  # format函数实现翻页
    # header在F12中的Network中，再刷新一下可以找到
    header = {
        'User-Agent': "Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/75.0.3770.142Safari/537.36"}
    req = requests.get(url, headers=header)  # 获取URL
    # print(req.text)  # 看网页源码
    return req.text
    # bs = BeautifulSoup(html, features="lxml")
    # texts = bs.find_all('ol', class_="grid_view")
    # print(texts)  # BeautifulSoup提取，内容类似于F12中的内容


def parse(text):  # 解析数据
    contents_staff = []
    contents_other = []
    html = etree.HTML(text)  # 初始化&标准化
    # xpath()返回**列表**
    # 一开始不知道是列表，又append到另一个列表里，导致有两层中括号，for循环只能算一个，使用replace会导致无法识别列表，只能算str
    # 因为源码含有多个div和span，需要标注序号；部分需要text()，否则会报错
    contents_title = html.xpath('//div[2]/div[@class="hd"]/a/span[1]/text()')
    contents_title_origin = html.xpath('//div[2]/div[@class="hd"]/a/span[2]/text()')
    contents_url = html.xpath('//div[2]/div[@class="hd"]/a/@href')
    contents_score = html.xpath('//div[2]/div[@class="bd"]/div/span[@class="rating_num"]/text()')
    # 此处contents_score = html.xpath('//div[2]/div[@class="bd"]/div[1]/span[2]/text()')也可以，用序号代替，注意从1开始
    contents_quote = html.xpath('//div[2]/div[@class="bd"]/p[2]/span[@class="inq"]/text()')
    contents_info = html.xpath('//div[2]/div[@class="bd"]/p[1]/text()')  # 日期也是有\xa0/\xa0出现，目前无法解决
    # print(contents_info)
    n = 0
    for data in range(len(contents_info)):
        if n % 2 == 0:
            contents_staff.extend(contents_info[n])
        else:
            contents_other.extend(contents_info[n])
        n += 1
    # print(contents_staff)
    # print(contents_other)
    # 这里的for会把每一个元素都遍历，一段话的每一个字都会被分开，就很离谱
    contents_txt = zip(contents_title, contents_title_origin, contents_url, contents_score, contents_staff,
                       contents_other, contents_quote)
    # zip()函数，contents=[(contents_title,contents_url， contents_score),()...]，是元组
    return contents_txt, contents_title, contents_title_origin, contents_url, contents_score, \
           contents_staff, contents_other, contents_quote


def write(data):
    raw_contents = getpage(data)  # 此处我遇到了一个问题：序号特别多，结果发现内容使用的是没有parse过的数据😓
    contents, titles, titles_origin, urls, scores, staff, other, quote = parse(raw_contents)
    title_lists.extend(titles)  # 将多个网页的内容拼接到一个列表
    title_origin_lists.extend(titles_origin)
    link_lists.extend(urls)
    score_lists.extend(scores)
    staff_lists.extend(staff)
    other_lists.extend(other)
    quote_lists.extend(quote)
    print(len(title_lists))
    print(len(title_origin_lists))
    print(len(link_lists))
    print(len(score_lists))
    print(len(staff_lists))
    print(len(other_lists))
    print(len(quote_lists))
    a = 0
    # 方法一(txt)：
    with open('douban_movie_top250(txt).txt', 'a', encoding='utf-8') as f:
        for content_tuple in contents:
            f.write("No " + str((i - 1) * 25 + a + 1) + ":\t")  # 序号
            a += 1
            # 不会正则表达式，不会分割，对\xa0/\xa0出现等问题使用比较原始的replace函数
            # # 我不是药神竟然没有quote， 也不知道元组怎么加，都失败了，懒得管了
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
    print(f"正在爬取第{i}页")  # 简化format函数

# 方法二(csv)：
b = 0
quote_lists.insert(134, ' ')  # 我不是药神竟然没有quote，害我搞了半天；txt烂泥扶不上墙，懒得管了，而且zip函数用的是元组，难顶
for aa in range(len(title_origin_lists)):
    title_origin_lists[aa].replace('?', '')
    title_origin_lists[aa].replace('/', '',1)
for x in range(len(title_lists)):
    number_lists.append(b + 1)
    b += 1
# contents_info = {'number': number_lists, 'name': title_lists, 'name_origin': title_origin_lists, 'link': link_lists,
#                  'score': score_lists, 'staff': staff_lists, 'other': other_lists, 'quote': quote_lists}
contents_info = {'number': number_lists, 'name': title_lists, 'name_origin': title_origin_lists, 'link': link_lists,
                 'score': score_lists, 'quote': quote_lists}
print(contents_info)
frame = pd.DataFrame(contents_info)  # csv文件
frame.to_csv(r'D:\programme_study\Python_work\crawler\douban_movie_top250(csv).csv')  # 乱码的话，记事本打开，转码ANSI
print(frame)
