from werkzeug.urls import url_parse

def is_absolute_url(url):
    return url_parse(url).netloc != ''