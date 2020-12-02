from urllib.parse import urlsplit


def get_domain(site_url: str):
    splitted_url = urlsplit(site_url)
    d = splitted_url.netloc
    return d


def clean_link(link):
    l = str(link).replace("'", "")
    return l


def is_content_valid(link, title):
    """
    Check for valid links

    :param link:
    :return:
    """
    # at least 3 slashes occurrences
    o = str(link).count('/')
    if o < 3:
        return False

    # at least 30 characters long
    l = len(str(link))
    if l < 30:
        return False

    # at least 15 characters in the title
    t = len(str(title))
    if t < 15:
        return False

    return True
