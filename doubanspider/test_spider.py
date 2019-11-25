import unittest

from .spider import DoubanSpider


class TestSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')
    def test_review_spider(self):
        spider = DoubanSpider()
        reviews = spider.access_review(26786669)
        self.assertTrue(len(reviews) > 0)




