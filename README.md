# HTTP Headers Hashing (HHHash)

HTTP Headers Hashing (HHHash) is a technique used to create a fingerprint of an HTTP server based on the headers it returns. HHHash employs one-way hashing to generate a hash value for the set of header keys returned by the server.

For more details about HHHash background, [HTTP Headers Hashing (HHHash) or improving correlation of crawled content](https://www.foo.be/2023/07/HTTP-Headers-Hashing_HHHash).

## Calculation of the HHHash

To calculate the HHHash, we concatenate the list of headers returned by the HTTP server. This list is ordered according to the sequence in which the headers appear in the server's response. Each header value is separated with `:`. 

The HHHash value is the SHA256 of the list.

## HHHash format

`hhh`:`1`:`20247663b5c63bf1291fe5350010dafb6d5e845e4c0daaf7dc9c0f646e947c29`

`prefix`:`version`:`SHA 256 value`

## Example

### Calculating HHHash from a curl command

Curl will attempt to run the request using HTTP2 by default. In order to get the same hash as the python requests module (which doesn't supports HTTP2), you need to specify the version with the `--http1.1` switch.

~~~bash
curl --http1.1 -s -D - https://www.circl.lu/ -o /dev/null  | awk 'NR != 1' | cut -f1 -d: | sed '/^[[:space:]]*$/d' | sed -z 's/\n/:/g' | sed 's/.$//' | sha256sum | cut -f1 -d " " | awk {'print "hhh:1:"$1'}
~~~

Output value
~~~
hhh:1:78f7ef0651bac1a5ea42ed9d22242ed8725f07815091032a34ab4e30d3c3cefc
~~~

## Limitations 

HHHash is an effective technique; however, its performance is heavily reliant on the characteristics of the HTTP client requests. Therefore, it is important to note that correlations between a set of hashes are typically established when using the same crawler or HTTP client parameters.

HTTP2 requires the [headers to be lowercase](https://www.rfc-editor.org/rfc/rfc7540#section-8.1.2). It will then changes the hash so you need to be aware of the HTTP version you're using.

### hhhash - Python Library

The [hhhash package](https://pypi.org/project/hhhash/) can be installed via a `pip install hhhash` or build with Poetry from this repository `poetry build` and `poetry install`.

#### Usage

~~~ipython
In [1]: import hhhash

In [2]: hhhash.buildhash(url="https://www.misp-lea.org", debug=False)
Out[2]: 'hhh:1:adca8a87f2a537dbbf07ba6d8cba6db53fde257ae2da4dad6f3ee6b47080c53f'

In [3]: hhhash.buildhash(url="https://www.misp-project.org", debug=False)
Out[3]: 'hhh:1:adca8a87f2a537dbbf07ba6d8cba6db53fde257ae2da4dad6f3ee6b47080c53f'

In [4]: hhhash.buildhash(url="https://www.circl.lu", debug=False)
Out[4]: 'hhh:1:334d8ab68f9e935f3af7c4a91220612f980f2d9168324530c03d28c9429e1299'

In [5]:
~~~

## Other libraries

- [c-hhhash](https://github.com/hrbrmstr/c-hhhash) - C++ HTTP Headers Hashing CLI
- [go-hhhash](https://github.com/hrbrmstr/go-hhhash) - golang HTTP Headers Hashing CLI
- [R hhhash](https://github.com/hrbrmstr/hhhash) - R library HHHash
