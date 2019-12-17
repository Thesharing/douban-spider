import unittest

from .spider import DoubanSpider
from .extract import *
from .extract.tag import *
from .extract.count import *
from .extract.score import *


class TestExtractors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')
        cls.review_content, cls.review_selector = cls.spider.access_brief(
            'https://movie.douban.com/subject/26786669/reviews')

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

    def test_extract_reviews(self):
        reviews = extract_reviews(self.review_selector)
        self.assertTrue(len(reviews) > 0)

    def test_extract_tag(self):
        tag_list = extract_tag(self.content)
        tag = tag_list['tag']
        seen = tag_list['seen']
        wish = tag_list['wish']
        self.assertTrue(len(tag) >= 8)
        self.assertTrue(seen >= 92568)
        self.assertTrue(wish >= 47687)

    def test_extract_score(self):
        res = extract_score(self.content)
        self.assertTrue(res['score'] > 0)
        self.assertTrue(res['reviewer'] > 84000)
        for i in range(5):
            self.assertTrue(res['detail'][str(i + 1)] > 0)
