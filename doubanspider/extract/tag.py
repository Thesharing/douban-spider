# 标签
# 人气 （看过 / 想看的数量）
import re

def extract_tag(content):
    result = {}
    word = re.compile('[\u4e00-\u9fa5_0-9]+')
    pattern = re.compile(r'\d+')
    tags = content.find('div', attrs={"class": "tags-body"}).text
    popularity = content.find_all('div', attrs={"class": "subject-others-interests-ft"})
    if len(word.findall(tags)):
        tags_list = word.findall(tags)
    else:
        tags_list = []

    if popularity[0].find(href=re.compile("collections")) is not None:
        if len(pattern.findall(popularity[0].find(href=re.compile("collections")).string)):
            seen = int(pattern.findall(popularity[0].find(href=re.compile("collections")).string)[0])
    else:
        seen = 0

    if popularity[0].find(href=re.compile("wishes")) is not None:
        if len(pattern.findall(popularity[0].find(href=re.compile("wishes")).string)):
            wish = int(pattern.findall(popularity[0].find(href=re.compile("wishes")).string)[0])
    else:
        wish = 0

    result['tag'] = tags_list
    result['seen'] = seen
    result['wish'] = wish

    return result
