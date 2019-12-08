import unittest

from .spider import DoubanSpider
from .extract import *


class TestSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')

    def test_review_spider(self):
        spider = DoubanSpider()
        review_pages = spider.access_review(26786669)
        reviews_pages = (page for page in review_pages)
        reviews_pages = list(reviews_pages)
        self.assertTrue(len(reviews_pages) > 0)
        if len(reviews_pages) > 1:
            self.assertNotEqual(reviews_pages[0], reviews_pages[1])

    def test_access_comment(self):
        spider = DoubanSpider()
        access_comment = spider.access_comment(26786669)
        self.assertTrue(len(access_comment)>0)
