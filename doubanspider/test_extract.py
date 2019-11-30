import unittest

from doubanspider.spider import DoubanSpider
from doubanspider.extract import *
from doubanspider.extract.score import *


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
        total_score = extract_score(self.content)['总评分']
        number_of_reviewers = extract_score(self.content)['评价人数']
        one = extract_score(self.content)['详情']['1']
        two = extract_score(self.content)['详情']['2']
        three = extract_score(self.content)['详情']['3']
        four = extract_score(self.content)['详情']['4']
        five = extract_score(self.content)['详情']['5']
        res = extract_score(self.content)
        print(res)
        self.assertEqual(type(total_score), float)
        self.assertEqual(type(number_of_reviewers), int)
        self.assertEqual(type(one), float)
        self.assertEqual(type(two), float)
        self.assertEqual(type(three), float)
        self.assertEqual(type(four), float)
        self.assertEqual(type(five), float)

if __name__=="__main__":
    unittest.main()