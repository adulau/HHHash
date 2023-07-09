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
