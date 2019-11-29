# 长影评
import re

def extract_reviews(html):
    """
    Extract the content of certain review based on review id.
    :param html: the content extracted from the full text page
    :return: reviews, reviews without pic, blanks,tags
    """
    content_pattern = re.compile('data-original(.*?)main-author', re.S)
    content = re.findall(content_pattern, html)
    reviews_pattern = re.compile('[\u4e00-\u9fa5|，、“”‘’：！~@#￥【】*（）——+。；？]+', re.S)
    reviews = re.findall(reviews_pattern, content[0])
    reviews = ''.join(reviews)
    #print(reviews)
    return reviews

