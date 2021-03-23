#导入函数库，从BeautifulSoup4导入BeautifulSoup函数库
from bs4 import BeautifulSoup
from random import randint
#导入requests函数库
import requests
import time
filename = 'spnovcp.txt'    #导入spnovcp作为输入文件
web_filename = 'spnov_web.txt'  #导入web_filename作为输出文件
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.79 Safari/537.36',
    'Connection': 'close'
}   #设置头部文件数据，设置为Chrome浏览器
try:
    kw = {'value1': 'ab', 'option1': 'fulltext'}    #创建新字典，命名为kw，（设置request.get传入参数,即搜索关键词）
    with open(filename) as file_object: #打开待搜索文件
        for line in file_object:    #逐行读入文件
            kw['value1'] = line     #搜索值重新赋值
            r = requests.get('https://www.microbiologyresearch.org/search', params=kw, headers = headers)   # 使用get方式搜索关键词数据，并请求网页赋值为r
            print(r.request.url)    #打印请求链接
            print(r.status_code)    #打印网页返回状态
            r.encoding = r.apparent_encoding    #更改编码类型
            data = BeautifulSoup(r.text, 'html.parser')     #使用BeautifulSoup解析r.text页面，并赋值为data
            paper_data = data.find('h4', class_='js-title resultItem__title accessIcons js-accessIcons')    #提取搜索页面中的第一个（搜索h4标签的关键词并赋值为paper_data）
            lev1_paper_data = paper_data.find('a')['href']      #提取第一个搜索结果中的链接
            print(lev1_paper_data)      #打印链接
            word = requests.get('https://www.microbiologyresearch.org'+lev1_paper_data)     #将请求到第一个的搜索结果用get方法请求页面，并赋值为word
            word_paper = BeautifulSoup(word.text, 'html.parser')    #使用BeautifulSoup解析word。text页面,并赋值为word_paper
            lev1_word_data = word_paper.find_all('span', class_='jp-italic')    #查找页面中所有含span标签，同时class=jp-italic的选项，并赋值为列表lev1_word_data
            doi_number_paper = word_paper.find('li', class_='article-meta-data__item item-meta-data__date-and-doi')     #查找页面中所有含li标签，同时查找doi的选项，并赋值为列表doi_number_paper
            doi_number = doi_number_paper.find('a')['href']     #提取doi编号
            print(doi_number)      #打印提取出的doi编号
            spnov_name_list = []    #创建新种列表
            spnov_name_list.append(lev1_word_data[2].text.strip())  #取出lev1_word_data的第三个值并除去空白赋值给spnov_name_list列表
            spnov_name_list.append(lev1_word_data[0].text.strip())  #取出lev1_word_data的第一个值并除去空白赋值给spnov_name_list列表
            spnov_names = list(set(spnov_name_list))        #去除列表中的重复部分
            spnov_name = ' '.join(spnov_names)      #列表转换为字符串并赋值给spnov_name
            print(spnov_name)   #打印spnov_name
            with open(web_filename, 'a') as web_filename_object:    #打开web_filename文件，逐行输入新种名字，DOi号，以及爬取的链接
                web_filename_object.write(spnov_name+ ', ' + doi_number.strip() + ', ' + word.request.url + '\n')
                t = randint(1, 20)  #设置随机休眠时间
                time.sleep(t)       #睡眠t秒
except:
    print("爬取失败")

