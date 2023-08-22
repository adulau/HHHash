import requests
import hashlib


def buildhash(url=None, debug=False, method='GET', timeout=5):
    """Build a HHHash from an HTTP request to specific url.

    Keyword arguments:
    - `url` -- the url to build the HHHash from the response headers (default None)
    - `debug` -- output the headers returned before hashing (default False)
    - `method` -- HTTP method to use (GET or HEAD) (default GET)
    - `timeout` -- default timeout for the connect/read timeout of request (default 2)

    For more details about the [HHHash algorithm](https://www.foo.be/2023/07/HTTP-Headers-Hashing_HHHash).
   """
    if url is None:
        return False
    if method == 'GET':
        r = requests.get(url, timeout=timeout, allow_redirects=False)
    elif method == 'HEAD':
        r = requests.head(url, timeout=timeout, allow_redirects=False)
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

def hash_from_banner(banner, debug=False):
    """Create a HHHash from an already fetched banner. Lines without colons will be skipped.

    Keyword arguments:
    - `banner` -- HTTP banner as a string
    - `debug` -- output the headers returned before hashing

    Example usage:

    ```
        >>> hash_from_banner('''HTTP/1.1 200 OK
        ... Content-Type: text/html; charset=ISO-8859-1
        ... Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-iV-j91UJEG2jNx4j6EeTug' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
        ... P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
        ... Date: Wed, 12 Jul 2023 20:23:42 GMT
        ... Server: gws
        ... X-XSS-Protection: 0
        ... X-Frame-Options: SAMEORIGIN
        ... Transfer-Encoding: chunked
        ... Expires: Wed, 12 Jul 2023 20:23:42 GMT
        ... Cache-Control: private
        ... Set-Cookie: <removed>
        ... Set-Cookie: <removed>
        ... Set-Cookie: <removed>
        ... Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000''')
        hhh:1:d9576f3e7a381562f7d18a514ab095fa8699e96891d346d0042f83e942373215

    ```
    """
    hhhash = ""
    for line in banner.splitlines():
        if ":" not in line:
            continue

        header, _ = line.split(":", maxsplit=1)
        hhhash = f"{hhhash}:{header.strip()}"
    if debug:
        print(hhhash[1:])
    m = hashlib.sha256()
    m.update(hhhash[1:].encode())
    digest = m.hexdigest()
    return f"hhh:1:{digest}"
