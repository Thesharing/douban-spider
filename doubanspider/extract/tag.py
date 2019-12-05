# 标签
# 人气 （看过 / 想看的数量）
import re

def extract_tag(content):
    """
            Extract tag and hotness of the movie.
            :param content: the content extracted by BeautifulSoup
            :return: dict[name: value], {'tag','seen','wish'}
        """

    result = {}
    tags = content.find('div', attrs={"class": "tags-body"}).text
    hotness = content.find('div', attrs={"class": "subject-others-interests-ft"}).text
    seen = hotness.split('\n')[1]
    wish = hotness.split('\n')[-2]

    if len(tags)!=0:
        tags_list = tags.split('\n')[1:-1]
    else:
        tags_list = []

    if len(hotness)!=0:
        seen = int(re.sub('\D','', seen))
        wish = int(re.sub('\D','', wish))
    else:
        seen = 0
        wish = 0

    result.update(tag=tags_list,seen=seen,wish=wish)
    return result
