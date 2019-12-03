import unittest

from doubanspider.extract.count import *
from .spider import DoubanSpider
from .extract import *


class TestExtractors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')

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

    def test_extract_data_count(self):
        res = extract_data_count(self.content)
        self.assertTrue(res['player'] >= 45)
        self.assertTrue(res['trailer'] >= 19)
        self.assertTrue(res['image'] >= 219)
        self.assertTrue(res['review']['short'] >= 26527)
        self.assertTrue(res['review']['long'] >= 513)
        self.assertTrue(res['discuss'] >= 292)
