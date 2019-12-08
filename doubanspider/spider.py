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
from .extract.review import extract_reviews


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

        # 返回某部电影短评 某一页的网页内容
        def access_comment_one_page(self, movie_id, start, sort="new_score", status="P"):
            """
            Return all comment of a comment page
            :param movie_id: the movie id
            :param sort: U - 近期热门, T - 标记最多, S - 评分最高, R - 最新上映
            :param start: start offset
            :param status: P - 已经看过, F - 没看过，但是想看
            :return:
            """
            url = str("https://movie.douban.com/subject/" + str(movie_id) + "/comments?start=" +
                      str(start) + "&limit=20&sort=" + sort + "&status=" + status + "&comments_only=1")
            # print(url)
            html = self._get(url, headers=HEADERS['comment'])
            soup = Soup(html, 'html.parser')
            print(soup)

            print("访问第" + str(int(start / 20)) + "页，返回的数据：")
            print({"html:": soup, "r": start / 20})
            return {"html:": soup, "r": start / 20}

    # 返回某部电影短评 所有页的网页内容（翻页一次调用一次前面的access_comment_one_page函数来获取某一页网页内容）
    def access_comment(self, movie_id, start=0, sort='new_score', status='P'):
        """
        crawl all comment of a movie from start page to last page
        :param movie_id: the movie id
        :param sort: U - 近期热门, T - 标记最多, S - 评分最高, R - 最新上映
        :param start: start offset
        :param status: P - 已经看过, F - 没看过，但是想看
        :return:
        """
        # 获取该电影的短评总数
        url = str("https://movie.douban.com/subject/" + str(movie_id) + "/comments?start=" +
                  str(start) + "&limit=20&sort=" + sort + "&status=" + status)
        # print(url)
        html = self._get(url, headers=HEADERS['comment'])
        soup = Soup(html, 'html.parser')
        temp = soup.find(class_='is-active')
        temp_list = filter(str.isdigit, str(temp))
        temp_string = "".join(temp_list)
        temp_number = int(temp_string)
        print("该电影的短评总数：" + str(temp_number))
        short_comments_number = temp_number

        res = []
        # 从第一页开始进行翻页，直到最后一页
        while start < short_comments_number:
            res.append(self.access_comment_one_page(movie_id, start, sort, status))
            start += 20
            print("已经访问过的的短评数目：" + str(start))

        return res

    def access_review(self, movie_id, start=0):
        """
        crawl all review pages of a movie from start page to last page
        :param movie_id:the movie id
        :param start:the start page
        :return:all review pages of a movie from the start page to last page
        """
        # ===========获取总页数============
        start_url = "https://movie.douban.com/subject/" + str(movie_id) + "/reviews"
        text = self._get(start_url, headers=HEADERS['page'])
        selector = Selector(text)
        total_page = int(selector.xpath('//span[@class="thispage"]/@data-total-page').extract()[0])
        # ==============翻页查询===========
        last_url = start_url
        for i in range(start, total_page):
            next_url = start_url + "?start=" + str(i * 20)
            header = HEADERS['page']
            header['Referer'] = last_url
            last_url = next_url
            text = self._get(next_url, headers=header)
            selector = Selector(text)
            yield selector

    def access_full_text(self, url):
        pass
