import unittest

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

    def test_extract_count(self):
        res = extract_count(self.content)
        self.assertTrue(res['player'] >= 45)
        self.assertTrue(res['trailer'] >= 19)
        self.assertTrue(res['image'] >= 219)
        self.assertTrue(res['review']['short'] >= 26527)
        self.assertTrue(res['review']['long'] >= 513)
        self.assertTrue(res['discuss'] >= 292)

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

    def test_extract_reviews(self):
        for selector in self.spider.access_review('26786669'):
            for review in extract_review_list(selector):
                self.assertTrue(review['comment'] > 0)
                self.assertTrue(review['upvote'] > 0)
                self.assertTrue(review['star'] > 0)
                self.assertTrue(len(review['username']) > 0)
                self.assertTrue(len(review['title']) > 0)
                self.assertTrue(len(review['time']) > 0)
                break
            break

    def test_extract_reviews_new(self):
        review = self.spider.access_review_text('10639399')
        html, text = extract_reviews_text(review)
        self.assertTrue(len(text) > 0)
