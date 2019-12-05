import unittest

from doubanspider.extract.comment import extract_comments
from doubanspider.headers import HEADERS
from .spider import DoubanSpider
from .extract import *


class TestExtractors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')
        cls.comments = cls.spider.access_comment(26786669)

    def test_extract_title(self):
        title, year = extract_title(self.content)
        self.assertEqual(title, '决战中途岛 Midway')
        self.assertEqual(year, 2019)

    def test_extract_summary(self):
        summary = extract_summary(self.selector)
        self.assertTrue(len(summary) > 0)

    def test_extract_info(self):
        info = extract_info(self.content)
        self.assertEqual(len(info), 11)

    def test_extract_comments(self):
        url = 'https://movie.douban.com/subject/26786669/comments?status=P'
        text = self.spider._get(url, headers=HEADERS['page'])
        results = extract_comments(text)
        self.assertTrue(len(results) > 0)

        return text
