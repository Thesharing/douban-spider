# 人气 （看过 / 想看的数量）
# 演员数量、预告片数量、图片数量、短评数量、长评数量、讨论区数量
import re


def extract_data_count(content):
    """
       Extract player count of the movie. if count is none default 0
       :param content: the content extracted by BeautifulSoup
       :return:  dict[name: value], {'player','trailer','image','review'{'short','long'},'discuss'}
    """
    res = {'review': {}}
    pattern = re.compile(r'\d+')
    celebrities = content.find('div', id='celebrities')
    related_pic = content.find('div', id='related-pic')
    comments_section = content.find('div', id='comments-section')
    review_section = content.find(attrs={"class": "reviews mod movie-content"})
    discuss = content.find(attrs={"class": "section-discussion"}).find_all(href=re.compile("discussion"))
    if celebrities.find(href=re.compile("celebrities")) is not None:
        if len(pattern.findall(celebrities.find(href=re.compile("celebrities")).string)):
            player_count = int(pattern.findall(celebrities.find(href=re.compile("celebrities")).string)[0])
        else:
            player_count = 0
    else:
        player_count = 0
    if related_pic.find(href=re.compile("trailer")) is not None:
        if len(pattern.findall(related_pic.find(href=re.compile("trailer")).string)):
            trailer_count = int(pattern.findall(related_pic.find(href=re.compile("trailer")).string)[0])
        else:
            trailer_count = 0
    else:
        trailer_count = 0
    if related_pic.find(href=re.compile("all_photos")) is not None:
        if len(pattern.findall(related_pic.find(href=re.compile("all_photos")).string)):
            image_count = int(pattern.findall(related_pic.find(href=re.compile("all_photos")).string)[0])
        else:
            image_count = 0
    else:
        image_count = 0
    if comments_section.find(href=re.compile("comments")) is not None:
        if len(pattern.findall(comments_section.find(href=re.compile("comments")).string)):
            short_review = int(pattern.findall(comments_section.find(href=re.compile("comments")).string)[0])
    else:
        short_review = 0
    if review_section.find(href=re.compile("reviews")) is not None:
        if pattern.findall(review_section.find(href=re.compile("reviews")).string)[0]:
            long_review = int(pattern.findall(review_section.find(href=re.compile("reviews")).string)[0])
        else:
            long_review = 0
    else:
        long_review = 0
    if len(discuss) != 0:
        if pattern.findall(discuss[len(discuss)-1].string) is not None:
            discuss_count = int(pattern.findall(discuss[len(discuss)-1].string)[0])
        else:
            discuss_count = 0
    res['player'] = player_count
    res['trailer'] = trailer_count
    res['image'] = image_count
    res['review']['short'] = short_review
    res['review']['long'] = long_review
    res['discuss'] = discuss_count
    return res
