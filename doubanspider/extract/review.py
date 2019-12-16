# 长影评
from bs4 import BeautifulSoup
import json
import jsonpath
from doubanspider.spider import DoubanSpider
from doubanspider.headers import *

def extract_reviews(id):
    """
    Extract the content of certain review based on review id
    :param html: the content extracted from the full text page
    :return: reviews, reviews without pic, blanks, tags
    """
    spider = DoubanSpider()
    url = 'https://movie.douban.com/j/review/' + str(id) + '/full'
    html = spider._get(url, headers = HEADERS['page'])
    unicodestr = json.loads(html)
    content = jsonpath.jsonpath(unicodestr, "$..html")
    full = content[0]
    soup = BeautifulSoup(full, 'lxml')
    text = soup.get_text()
    text = text.replace('\n', '')
    reviews = {}
    reviews['full'] = full
    reviews['text'] = text

    return reviews