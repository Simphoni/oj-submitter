#!/usr/bin/python3

prime = [
    30000023611
]
salt = [
    25190143790
]
length = [11]
base = 200


def encrypt(str):
    Num = 0
    for i in str:
        Num = Num * base + ord(i) + 1
    res = 0
    for i in range(0, len(prime)):
        mo = (Num + salt[i]) % prime[i]
        mo = pow(mo, prime[i] - 2, prime[i])
        res = res * (233 + 10 ** length[i]) + mo
    return hex(res)


def exgcd(a, b):
    if b == 0:
        return (1, 0)
    res = exgcd(b, a % b)
    tmp = res[0]
    x = res[1]
    y = tmp - (a // b) * x
    return (x, y)


def decrypt(str):
    Num = int(str, 16)
    a, mod = 0, 1
    for i in range(len(prime) - 1, -1, -1):
        mo = Num % (233 + 10 ** length[i])
        Num //= 233 + 10 ** length[i]
        mo = pow(mo, prime[i] - 2, prime[i])
        mo = (mo + prime[i] - salt[i]) % prime[i]
        tup = exgcd(mod, prime[i])
        a += tup[0] * mod * (mo - a)
        mod *= prime[i]
        a = (a % mod + mod) % mod
    ret = ''
    while a > 0:
        ret = chr(a % base - 1) + ret
        a //= base
    return ret
