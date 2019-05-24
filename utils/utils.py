from urllib.parse import urlsplit


def get_domain(site_url: str):
    splitted_url = urlsplit(site_url)
    d = splitted_url.netloc
    return d
