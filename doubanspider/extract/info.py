def extract_info(content):
    """
    Extract basic info of the movie.
    :param content: the content extracted by BeautifulSoup
    :return: dict[name: value], the basic info attributes of the movie
    """
    info = content.find('div', id='info')
    res = {}
    for item in info.text.strip().split('\n'):
        attr = item.split(': ')
        res[attr[0]] = attr[1]
    return res
