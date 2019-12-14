# 短影评
from bs4 import BeautifulSoup as Soup


def extract_comments(text):
    results = []
    for div in soup.select('#comments > div.comment-item'):
        username = div.select_one('h3 > span.comment-info > a').get_text(strip=True)
        time = div.select_one('h3 > span.comment-info > span.comment-time').get_text(strip=True)
        rating = div.select_one('h3 > span.comment-info > span.rating')
        star = None
        if rating is not None:
            star = rating.get('class')[0].replace('allstar', '')
        vote = div.select_one('h3 > span.comment-vote > span.votes').get_text(strip=True)
        content = div.select_one('div.comment > p').get_text(strip=True)
        results.append({
            'username': username,
            'star': str(int(int(star) / 10)),
            'time': time,
            'vote': vote,
            'content': content
        })
        yield results
    return 'done'
