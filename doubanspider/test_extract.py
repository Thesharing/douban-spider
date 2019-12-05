import unittest

from .spider import DoubanSpider
from .extract import *
from .extract.tag import *

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

    def test_extract_tag(self):
        tagList = extract_tag(self.content)
        tag = tagList['tag']
        seen = tagList['seen']
        wish = tagList['wish']
        self.assertTrue(len(tag) >= 8)
        self.assertTrue(seen >= 92568)
        self.assertTrue(wish >= 47687)
