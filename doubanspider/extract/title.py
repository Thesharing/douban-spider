def extract_title(content):
    """
    Extract title of the movie.
    This illustrates how to extract text via BeautifulSoup.
    The doc: https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/
    :param content: the content extracted by BeautifulSoup
    :return: tuple[str], title and year of the movie
    """
    h1 = content.find('h1')
    span = h1.find('span')
    title = span.text
    span = span.find_next('span')
    year = int(span.text[1:-1]) if span is not None else None
    return title, year
