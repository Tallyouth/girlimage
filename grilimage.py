import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from multiprocessing import Pool
def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
            'Referer': 'http://www.mzitu.com'
        }
        res = requests.get(url, headers=headers)
        if res.status_code ==200:
            return res.text
        return None
    except RequestException:
        return None
def main():
    url = 'http://www.mzitu.com/'
    html = get_page(url)
    list = parse_page(html)
    for url in list:
        htmls = scrapy_page(url)
        a = int(get_image_number(htmls)) + 1
        for i in range(1, a):
            urls = url + '/{}'.format(i)
            res = get_page(urls)
            text = pq(res)
            image_title = text('.main-title').text()
            image_url = text('.main-image  p  a img').attr('src')
            image = down_load(image_url)
            save_image(image, image_title)
def parse_page(html):
    list = []
    doc = pq(html)
    items = doc('li').items()
    if items:
        for item in items:
            url = item.find('span a[target="_blank"]').attr('href')
            if url:
                list.append(url)
    return list
def down_load(url):
    try:
        print('正在下载图片', url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
            'Referer': 'http://i.meizitu.net'
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.content
        return None
    except RequestException:
        print('下载出错')
        return None
def scrapy_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
            'Host': 'www.mzitu.com',
            'Referer': 'http://www.mzitu.com'
        }
        res = requests.get(url, headers=headers)
        if res.status_code ==200:
            return res.text
        return None
    except RequestException:
        return None
def get_image_number(htmls):
    doc = pq(htmls)
    item = doc('.pagenavi a span').items()
    a=[]
    for i in item:
        a.append(i.text())
    number = a[-2]
    return number
def save_image(image, title):
    file_path = 'C:/Users/lenovo1/Desktop/python2/meitu/{0}.{1}'.format(title, 'jpg')
    with open(file_path, 'wb') as f:
        f.write(image)
        f.close()
if __name__ == '__main__':
    pool = Pool(5)
    for i in range(5):
        pool.apply_async(main, args=())
    pool.close()
    pool.join()
    print('图片下载完成')

