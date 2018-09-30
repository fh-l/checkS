#!/usr/bin/env python
# encoding: utf-8
'''
@author: yao.qiang
@contact: yao.qiang@sihuatech.com
@file: utils.py
@time: 2018/9/21 17:17
@desc:
'''
from __future__ import print_function
from hashlib import sha1
import hmac
import base64

def hash_hmac(code, key):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
    return base64.b64encode(hmac_code).decode()

if __name__ == '__main__':
    print(hash_hmac('GET&Version=4.0&Date=2018-09-05 15:00:00', '123'))