import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None
def parse_page_index(html ):
    data = json.loads(html)
    if data and 'data' in data.keys():# data.keys()获取data所有的键
        for item in data.get('data'):
            yield item.get('article_url')
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错')
        return None
def parse_page_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select('title')[0].text
    print(title)
def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            parse_page_detail(html)
if __name__ == '__main__':
    main()




