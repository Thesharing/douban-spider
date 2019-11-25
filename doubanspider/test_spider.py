import unittest

from .spider import DoubanSpider


class TestSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        # cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')

    # 测试 access_comment
    def test_access_comment(self):
        spider = DoubanSpider()
        spider.access_comment(26786669)
