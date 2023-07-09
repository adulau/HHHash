# HTTP Headers Hashing (HHHash)

HTTP Headers Hashing (HHHash) is a technique used to create a fingerprint of an HTTP server based on the headers it returns. HHHash employs one-way hashing to generate a hash value for the set of header keys returned by the server

## Calculation of the HHHash

To calculate the HHHash, we concatenate the list of headers returned by the HTTP server. This list is ordered according to the sequence in which the headers appear in the server's response. Each header value is separated with `:`. 

The HHHash value is the SHA256 of the list.

## HHHash format

`hhh`:`1`:`20247663b5c63bf1291fe5350010dafb6d5e845e4c0daaf7dc9c0f646e947c29`

`prefix`:`version`:`SHA 256 value`

## Example

### Calculating HHHash from a curl command

~~~
$ curl -s -D - https://www.circl.lu/ -o /dev/null  | awk 'NR != 1' | cut -f1 -d: | sed '/^[[:space:]]*$/d' | sed -z 's/\n/:/g' | sha256sum | cut -f1 -d " " | awk {'print "hhh:1:"$1'}
~~~

Output value
~~~
hhh:1:79dde6169456e7e2886eb1668b3c27e8438f1a7219fc5fbb13d9c8eec07c5983
~~~
