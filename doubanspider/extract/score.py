# 评分和评分人数等详情
import re


def extract_score(content):
    """
        Extract score of the movie.
        :param content: the content extracted by BeautifulSoup
        :return: dict[name: value], {'总评分','评价人数','详情'{'1','2','3','4','5'}}
    """

    res = {'详情': {}}
    pattern = re.compile(r'\d+')
    decimal = re.compile(r'\d+.*\d+')
    rating_num = content.find('strong', attrs={"class": "ll rating_num"})
    rating_people = content.find('a', attrs={"class": "rating_people"})
    stars = content.find_all('span', attrs={"class": "rating_per"})
    if decimal.findall(rating_num.string)[0]:
        total_score = float(decimal.findall(rating_num.string)[0])
    else:
        total_score = 0
    if pattern.findall(rating_people.find(attrs={"property": "v:votes"}).string)[0]:
        number_of_reviewers = int(pattern.findall(rating_people.find(attrs={"property": "v:votes"}).string)[0])
    else:
        number_of_reviewers = 0
    if decimal.findall(stars[4].string)[0]:
        one = float(decimal.findall(stars[4].string)[0])
    else:
        one = 0
    if decimal.findall(stars[3].string)[0]:
        two = float(decimal.findall(stars[3].string)[0])
    else:
        two = 0
    if decimal.findall(stars[2].string)[0]:
        three = float(decimal.findall(stars[2].string)[0])
    else:
        three = 0
    if decimal.findall(stars[1].string)[0]:
        four = float(decimal.findall(stars[1].string)[0])
    else:
        four = 0
    if decimal.findall(stars[0].string)[0]:
        five = float(decimal.findall(stars[0].string)[0])
    else:
        five = 0

    res['总评分'] = total_score
    res['评价人数'] = number_of_reviewers
    res['详情']['1'] = one
    res['详情']['2'] = two
    res['详情']['3'] = three
    res['详情']['4'] = four
    res['详情']['5'] = five

    return res
