from doubanspider import DoubanSpider
from doubanspider.test_spider import TestSpider

if __name__ == '__main__':
    spider = DoubanSpider()

    # TestSpider
    tspider = TestSpider()
    tspider.test_access_comment()