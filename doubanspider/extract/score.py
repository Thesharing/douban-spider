# 评分和评分人数等详情

import re

pattern = re.compile(r'\d+')
decimal = re.compile(r'\d+.*\d+')


def extract_score(content):
    """
    Extract score of the movie.

    :param content: the content extracted by BeautifulSoup
    :return: dict[name: value], {'总评分','评价人数','详情'{'1','2','3','4','5'}}
    """
    star = []
    rating_num = content.find('strong', attrs={"class": "ll rating_num"})
    rating_people = content.find('a', attrs={"class": "rating_people"})
    reviewers = rating_people.find(attrs={"property": "v:votes"})
    stars = content.find_all('span', attrs={"class": "rating_per"})
    total_score = float(decimal.findall(rating_num.string)[0]) if decimal.findall(rating_num.string)[0] else 0
    number_of_reviewers = int(pattern.findall(reviewers.string)[0]) if pattern.findall(reviewers.string)[0] else 0

    for i in range(5):
        star.append(float(decimal.findall(stars[4 - i].string)[0]) if decimal.findall(stars[4 - i].string)[0] else 0)

    res = {'score': total_score, 'reviewer': number_of_reviewers, 'detail': {str(i + 1): star[i] for i in range(5)}}

    return res
