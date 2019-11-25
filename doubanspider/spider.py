import json
import time
from typing import List

import brotli

# Parsers
import re
from bs4 import BeautifulSoup as Soup
from parsel import Selector

from spiderutil.network import Session

from .headers import HEADERS
from .extract.review import extract_reviews

class DoubanSpider:

    def __init__(self, session: Session = None):
        self.session = Session(retry=5, timeout=10) if session is None else session

    def list(self, tags: List[str] = None, sort: str = 'U', start: int = 0, limit: int = 100000):
        """
        Return the list of URLs.
        :param sort: U - 近期热门, T - 标记最多, S - 评分最高, R - 最新上映
        :param tags: All the tags showed on the page
        :param start: start offset
        :param limit: limit to end
        :return:
        """
        url = 'https://movie.douban.com/j/new_search_subjects'
        while start < limit:
            params = {
                'sort': sort,
                'range': '0, 10',
                'tags': ','.join(tags) if tags is not None else '',
                'start': start
            }
            text = self._get(url, params=params, headers=HEADERS['api'])
            data = json.loads(text)['data']
            for item in data:
                yield item['url']
            time.sleep(2)

    def _get(self, url, **kwargs):
        r = self.session.get(url, **kwargs)
        if r.headers['Content-Encoding'] == 'br':
            return brotli.decompress(r.content).decode('utf-8')
        else:
            return r.text

    def access_brief(self, url):
        """
        Crawl the brief page
        :param url:
        :return:
        """

        text = self._get(url, headers=HEADERS['page'])
        soup = Soup(text, 'lxml')
        content = soup.find('div', id='content')
        selector = Selector(text)
        return content, selector

    def access_celebrity(self, movie_id):
        pass

    def access_comment(self, movie_id, start=0, sort='new_score', status='P'):
        pass

    def access_review(self, movie_id, start=0):
        """
        crawl all reviews of a movie from start page to last page
        :param movie_id:the movie id
        :param start:the start page
        :return:all reviews of a movie from the start page to last page
        """
        all_reviews = []
        # ===========获取总页数============
        start_url = "https://movie.douban.com/subject/" +str(movie_id) + "/reviews"
        text = self._get(start_url, headers=HEADERS['page'])
        selector = Selector(text)
        total_page = int(selector.xpath('//span[@class="thispage"]/@data-total-page').extract()[0])
        #==============翻页查询===========
        last_url = start_url
        for i in range(start,total_page + 1):
            next_url = start_url + "?start=" + str(i * 20)
            header = HEADERS['page']
            header['Referer'] = last_url
            text = self._get(next_url, headers=header)
            selector = Selector(text)
            # 获取当前页所有的评论数，包括折叠的
            page_reviews = extract_reviews(selector)
            for item in page_reviews:
                all_reviews.append(item)
            last_url = next_url

        return all_reviews

    def access_full_text(self, url):
        pass
