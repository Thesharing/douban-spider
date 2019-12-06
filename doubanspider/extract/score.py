# 评分和评分人数等详情
import re


def extract_score(content):
    """
        Extract score of the movie.
        :param content: the content extracted by BeautifulSoup
        :return: dict[name: value], {'总评分','评价人数','详情'{'1','2','3','4','5'}}
    """
    star = []
    pattern = re.compile(r'\d+')
    decimal = re.compile(r'\d+.*\d+')
    rating_num = content.find('strong', attrs={"class": "ll rating_num"})
    rating_people = content.find('a', attrs={"class": "rating_people"})
    reviewers = rating_people.find(attrs={"property": "v:votes"})
    stars = content.find_all('span', attrs={"class": "rating_per"})
    total_score = decimal.findall(rating_num.string)[0] if (decimal.findall(rating_num.string)[0]) else 0
    number_of_reviewers = pattern.findall(reviewers.string[0]) if (pattern.findall(reviewers.string)[0]) else 0

    for i in range(5):
        star.append(decimal.findall(stars[4-i].string)[0] if(decimal.findall(stars[4-i].string)[0]) else 0)

    res = {'总评分': total_score, '评价人数': number_of_reviewers, '详情': {'1': star[0], '2': star[1], '3': star[2], '4': star[3], '5': star[4]}}

    return res
