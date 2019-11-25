import json
import time
from typing import List

import brotli

# Parsers
import re
from bs4 import BeautifulSoup as Soup
from parsel import Selector
from selenium import webdriver

from spiderutil.network import Session

from .headers import HEADERS


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
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        soup = Soup(html, "html.parser")
        # print(soup.pre.string)
        driver.close()

        print("访问第"+str(int(start/20))+"页，返回的数据：")
        print({"html:": soup.pre.string, "r": start / 20})
        return {"html:": soup.pre.string, "r": start / 20}

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
        driver = webdriver.Chrome()
        driver.get(url)
        html = driver.page_source
        soup = Soup(html, "html.parser")
        temp = soup.find(class_='is-active')
        temp_list = filter(str.isdigit, str(temp))
        temp_string = "".join(temp_list)
        temp_number = int(temp_string)
        print("该电影的短评总数："+str(temp_number))
        short_comments_number = temp_number

        # 从第一页开始进行翻页，直到最后一页
        while start < short_comments_number:
            self.access_comment_one_page(movie_id, start, sort, status)
            start += 20
            print("已经访问过的的短评数目："+str(start))
        return

    def access_review(self, movie_id, start=0):
        pass

    def access_full_text(self, url):
        pass
