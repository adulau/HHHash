import requests
import hashlib


def buildhash(url=None, debug=False, method='GET', timeout=5):
    """Build a HHHash from an HTTP request to specific url.

    Keyword arguments:
    url -- the url to build the HHHash from the response headers (default None)
    debug -- output the headers returned before hashing (default False)
    method -- HTTP method to use (GET or HEAD) (default GET)
    timeout -- default timeout for the connect/read timeout of request (default 2)
    """
    if url is None:
        return False
    if method == 'GET':
        r = requests.get(url, timeout=timeout)
    elif method == 'HEAD':
        r = requests.head(url, timeout=timeout)
    else:
        return False
    hhhash = ""
    for header in r.headers.keys():
        hhhash = f"{hhhash}:{header}"
    m = hashlib.sha256()
    if debug:
        print(hhhash[1:])
    m.update(hhhash[1:].encode())
    digest = m.hexdigest()
    return f"hhh:1:{digest}"
