# 长影评
import re

# 文字与星级的映射
star_to_level = {"很差": 1, "较差": 2, "还行": 3, "推荐": 4, "力荐": 5}


def extract_reviews(selector):
    """
    extract all reviews of a review page
    :param selector:the selector of a review page
    :return:all reviews of a review page
    """
    page_reviews = []
    review_list = selector.xpath('//div[@class="main review-item"]')
    review_num = len(review_list)
    # 解析每一条评论
    for i in range(review_num):
        review_content = review_list[i]
        review = extract_review(review_content)
        page_reviews.append(review)
    return page_reviews


def extract_review(selector):
    """
    extract a review
    :param selector:the selector of a review
    :return:a review parse result
    """
    header = selector.xpath('./header')
    body = selector.xpath('./div')
    username = header.xpath('./a[@class="name"]/text()').extract()[0]
    star = header.xpath('./span/@title').extract()
    if len(star) == 0:
        # 没有星级
        star = "null"
    else:
        star = star_to_level[star[0]]
    time = header.xpath('./span[@class="main-meta"]/text()').extract()[0]
    title = body.xpath('./h2/a/text()').extract()[0]
    url = body.xpath('./h2/a/@href').extract()[0]
    upvote = body.xpath('./div[@class="action"]/a[@class="action-btn up"]/span/text()').extract()[0].strip()
    if len(upvote) == 0:
        # 没有upvote
        upvote = 0
    downvote = body.xpath('./div[@class="action"]/a[@class="action-btn down"]/span/text()').extract()[0].strip()
    if len(downvote) == 0:
        # 没有downvote
        downvote = 0
    p = re.compile(r'\d+')
    comment = p.findall(body.xpath('./div[@class="action"]/a[@class="reply "]/text()').extract()[0])[0]
    full = body.xpath('./div[@class="review-short"]/@data-rid').extract()[0]
    review = {'username': username, "star": star, 'time': time, 'title': title, 'url': url, 'upvote': upvote,
              'downvote': downvote, 'comment': comment, 'full': full}

    return review
