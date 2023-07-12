import requests
import hashlib


def buildhash(url=None, debug=False):
    if url is None:
        return False
    r = requests.get(url)
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
    """This allows the creation of hhhash without a request, if the banner string is already available
    
    Example:
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
    """
    hhhash = ""
    for line in banner.splitlines():
        if line[:4] == "HTTP":
            continue
        key = line
        if ":" in key:
            key, _ = line.split(":", maxsplit=1)
        hhhash = f"{hhhash}:{key.strip()}"
    if debug:
        print(hhhash[1:])
    m = hashlib.sha256()
    m.update(hhhash[1:].encode())
    digest = m.hexdigest()
    return f"hhh:1:{digest}"
