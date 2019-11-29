import json
import time
from typing import List

import brotli
import urllib3
from packaging import version

# Parsers
import re
from bs4 import BeautifulSoup as Soup
from parsel import Selector

from spiderutil.network import Session

from .headers import HEADERS


class DoubanSpider:

    def __init__(self, session: Session = None):
        self.session = Session(retry=5, timeout=10) if session is None else session
        self.ENABLE_BROTLI = version.parse(urllib3.__version__) < version.parse('1.25.1')

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
        if r.headers['Content-Encoding'] == 'br' and self.ENABLE_BROTLI:
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
        pass

    def access_full_text(self, url):
        """
        Crawl the full text page
        :param url: 'https://movie.douban.com/j/review/full_text_id/full'  full_text_id is from review page
        :return:
        """
        full_text = self._get(url, headers=HEADERS['page'])
        return full_text

