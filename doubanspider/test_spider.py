import unittest

from .spider import DoubanSpider


class TestSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')

    def test_celebrity(self):
        celebrities = self.spider.access_celebrity("26786669")
        self.assertTrue(len(celebrities) > 0)