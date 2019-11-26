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
        player = extract_data_count(self.content)['player']
        trailer = extract_data_count(self.content)['trailer']
        image = extract_data_count(self.content)['image']
        short_review=extract_data_count(self.content)['review']['short']
        long_review = extract_data_count(self.content)['review']['long']
        discuss = extract_data_count(self.content)['discuss']
        self.assertEqual(type(player), int)
        self.assertEqual(type(trailer), int)
        self.assertEqual(type(image), int)
        self.assertEqual(type(short_review), int)
        self.assertEqual(type(long_review), int)
        self.assertEqual(type(discuss), int)
