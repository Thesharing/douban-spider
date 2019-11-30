import unittest

from doubanspider.spider import DoubanSpider
from doubanspider.extract import *
from doubanspider.extract.tag import *

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

    def test_extract_score(self):
        tag = extract_tag(self.content)['tag']
        seen = extract_tag(self.content)['seen']
        wish = extract_tag(self.content)['wish']
        self.assertEqual(type(tag), list)
        self.assertEqual(type(seen), int)
        self.assertEqual(type(wish), int)