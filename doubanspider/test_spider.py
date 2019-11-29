import unittest

from .spider import DoubanSpider


class TestSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')

    def test_access_full_text(self):
        full_text = self.spider.access_full_text('https://movie.douban.com/j/review/10639399/full')
        self.assertTrue(len(full_text) > 0)
