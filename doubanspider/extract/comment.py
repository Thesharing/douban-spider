def extract_comments(soup):
    """
    短影评
    :param soup:
    :return:
    """
    for div in soup.select('#comments > div.comment-item'):
        username = div.select_one('h3 > span.comment-info > a').get_text(strip=True)
        time = div.select_one('h3 > span.comment-info > span.comment-time').get_text(strip=True)
        rating = div.select_one('h3 > span.comment-info > span.rating')
        star = 0
        if rating is not None:
            star = rating.get('class')[0].replace('allstar', '')
        vote = div.select_one('h3 > span.comment-vote > span.votes').get_text(strip=True)
        vote = int(vote) if len(vote) > 0 else 0
        content = div.select_one('div.comment > p').get_text(strip=True)
        yield {
            'username': username,
            'star': int(star) / 10,
            'time': time,
            'vote': vote,
            'content': content
        }
