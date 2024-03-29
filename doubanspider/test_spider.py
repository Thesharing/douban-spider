import unittest

from .spider import DoubanSpider


class TestSpider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = DoubanSpider()
        cls.content, cls.selector = cls.spider.access_brief('https://movie.douban.com/subject/26786669/')

    def test_review_spider(self):
        review_pages = self.spider.access_review(26786669)
        reviews_pages = (page for page in review_pages)
        reviews_pages = list(reviews_pages)
        self.assertTrue(len(reviews_pages) > 0)
        if len(reviews_pages) > 1:
            self.assertNotEqual(reviews_pages[0], reviews_pages[1])

    def test_celebrity(self):
        celebrities = self.spider.access_celebrity("26786669")
        self.assertTrue(len(celebrities) > 0)

    def test_access_comment(self):
        access_comment = self.spider.access_comment(26786669)
        self.assertTrue(len(next(access_comment)) > 0)
