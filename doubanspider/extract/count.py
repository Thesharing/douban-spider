# 人气 （看过 / 想看的数量）
# 演员数量、预告片数量、图片数量、短评数量、长评数量、讨论区数量
import re


def extract_data_count(content):
    """
       Extract player count of the movie. if count is none default 0
       :param content: the content extracted by BeautifulSoup
       :return:  dict[name: value], {'player','trailer','image','review'{'short','long'},'discuss'}
    """
    celebrities = content.find('div', id='celebrities').find('a')
    related_pic = content.find('div', id='related-pic').find(attrs={"class": "pl"})
    trailer = related_pic.find('a', href=re.compile("trailer"))
    image = related_pic.find('a', href=re.compile("all_photos"))
    short_review_section = content.find('div', id='comments-section').find(attrs={"class": "pl"})
    short_review=short_review_section.contents[1]
    long_review_section = content.find(attrs={"class": "reviews mod movie-content"}).find(attrs={"class": "pl"})
    long_review=long_review_section.contents[1]
    discuss = content.find(attrs={"class": "section-discussion"}).find('p',attrs={"class": "pl"})
    discuss_more = discuss.contents[1]
    try:
        player_count = int(celebrities.string.strip('全部'))
    except Exception:
        player_count = 0
    try:
        trailer_count = int(trailer.string.strip('预告片'))
    except Exception:
        trailer_count = 0
    try:
        image_count = int(image.string.strip('图片'))
    except Exception:
        image_count = 0
    try:
        short_review_count = int(short_review.string.strip('全部').strip('条'))
    except Exception:short_review_count=0
    try:
        long_review_count = int(long_review.string.strip('全部').strip('条'))
    except Exception:long_review_count=0
    try:
        discuss_count = int(re.findall(r'\d+',discuss_more.string)[0])
    except Exception:discuss_count=0
    keys = ['player', 'trailer', 'image', 'discuss']
    values = [player_count, trailer_count, image_count, discuss_count]
    review_keys = ['short', 'long']
    review_value = [short_review_count, long_review_count]
    res = {key: value for key, value in zip(keys, values)}
    res['review'] = {key: value for key, value in zip(review_keys, review_value)}
    return res
