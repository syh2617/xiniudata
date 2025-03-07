#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 苏玉恒
# @time    : 2025/3/7 下午8:55
# @function: the script is used to do something.
# @version : V1
import hashlib
import json

_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
_p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O"


def u_a(e):
    e = ''.join([c for c in e if c in _keyStr])
    u = ""
    c = 0
    while c < len(e):
        t = _keyStr.index(e[c]) << 2
        c += 1
        o = _keyStr.index(e[c])
        t |= o >> 4
        c += 1
        n = (15 & o) << 4
        i = _keyStr.index(e[c])
        n |= i >> 2
        c += 1
        r = (3 & i) << 6
        a = _keyStr.index(e[c])
        r |= a
        c += 1
        u += chr(t)
        if i != 64:
            u += chr(n)
        if a != 64:
            u += chr(r)
    return u


def _u_d(e):
    t = ""
    n = 0
    while n < len(e):
        r = ord(e[n])
        if r < 128:
            t += chr(r)
            n += 1
        elif 191 < r < 224:
            o = ord(e[n + 1])
            t += chr((31 & r) << 6 | 63 & o)
            n += 2
        else:
            o = ord(e[n + 1])
            i = ord(e[n + 2])
            t += chr((15 & r) << 12 | (63 & o) << 6 | 63 & i)
            n += 3
    return t


def u_b(e):
    t = ""
    for n in range(len(e)):
        r = ord(_p[n % len(_p)])
        t += chr(ord(e[n]) ^ r)
    return _u_d(t)


def get_answer(r):
    l = r['v']
    s = r['d']
    if l == 2:
        d = u_a(s)
        y = u_b(d)
        v = y
        return v
    elif l == 1:
        d = u_a(s)
        y = u_b(d)
        v = json.loads(y)
        return v


def u_c(e):
    if e is None:
        return None
    c = ""
    l = 0
    while l < len(e):
        t = ord(e[l])
        l += 1
        o = t >> 2
        if l < len(e):
            n = ord(e[l])
            l += 1
            i = (3 & t) << 4 | n >> 4
            if l < len(e):
                r = ord(e[l])
                l += 1
                a = (15 & n) << 2 | r >> 6
                u = 63 & r
            else:
                a = (15 & n) << 2
                u = 64
        else:
            i = (3 & t) << 4
            a = 64
            u = 64
        c += _keyStr[o] + _keyStr[i] + _keyStr[a] + _keyStr[u]
    return c


def u_d(e):
    if e is None:
        return None
    t = ""
    for n in range(len(e)):
        r = ord(_p[n % len(_p)])
        t += chr(ord(e[n]) ^ r)
    return t


def sig(e):
    return hashlib.md5((e + _p).encode()).hexdigest().upper()


def get_payload_sig(n):
    l = json.dumps(n)
    s = json.loads(l)
    f = u_c(u_d(json.dumps(s)))
    p = sig(f)
    s['payload'] = f
    s['sig'] = p
    return s


if __name__ == '__main__':
    payload_pro = {
        "sort": 1,
        "start": 40,
        "limit": 20
    }
    print(get_payload_sig(payload_pro))