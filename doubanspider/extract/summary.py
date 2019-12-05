def extract_summary(selector):
    """
    Extract the summary of the movie.
    This illustrates how to extract text via Parsel selector and XPath.
    The doc of Parsel: https://parsel.readthedocs.io/en/latest/
    The cheatsheet of XPath: https://devhints.io/xpath
    :param selector: the selector extracted by Parsel
    :return: str, the summary of the movie
    """
    text = selector.xpath('//span[@property="v:summary"]/text()').get()
    if text is not None:
        return text.strip()
    else:
        return None
