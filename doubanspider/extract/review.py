# 长影评
import re
from bs4 import BeautifulSoup

# 文字与星级的映射
star_to_level = {"很差": 1, "较差": 2, "还行": 3, "推荐": 4, "力荐": 5}


def extract_review_list(selector):
    """
    extract all reviews of a review page
    :param selector:the selector of a review page
    :return:all reviews of a review page
    """
    review_list = selector.xpath('//div[@class="main review-item"]')
    # 解析每一条评论
    for review_content in review_list:
        review = extract_review_item(review_content)
        yield review


def extract_review_item(selector):
    """
    extract a review
    :param selector:the selector of a review
    :return:a review parse result
    """
    header = selector.xpath('./header')
    body = selector.xpath('./div')
    username = header.xpath('./a[@class="name"]/text()').extract()[0]
    star = header.xpath('./span/@title').extract()
    star = star_to_level[star[0]] if len(star) > 0 else 0
    time = header.xpath('./span[@class="main-meta"]/text()').extract()[0]
    title = body.xpath('./h2/a/text()').extract()[0]
    url = body.xpath('./h2/a/@href').extract()[0]
    upvote = body.xpath('./div[@class="action"]/a[@class="action-btn up"]/span/text()').extract()[0].strip()
    upvote = 0 if len(upvote) == 0 else int(upvote)
    downvote = body.xpath('./div[@class="action"]/a[@class="action-btn down"]/span/text()').extract()[0].strip()
    downvote = int(downvote) if len(downvote) > 0 else 0
    p = re.compile(r'\d+')
    comment = p.findall(body.xpath('./div[@class="action"]/a[@class="reply "]/text()').extract()[0])[0].strip()
    comment = int(comment) if len(comment) > 0 else 0
    full = body.xpath('./div[@class="review-short"]/@data-rid').extract()[0]
    review = {'username': username, "star": star, 'time': time, 'title': title, 'upvote': upvote,
              'downvote': downvote, 'comment': comment, 'full': full}

    return review


def extract_reviews_text(html):
    """
    Extract the content of certain review based on review id
    :param html: the content extracted from the full text page
    :return: reviews, reviews without pic, blanks, tags
    """
    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text()
    text = text.replace('\n', '')
    return html, text
