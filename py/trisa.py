import string
import pickle
import numpy as np
from hashlib import blake2b

import pybitcointools as vbtc

trisa_pii_set = ['name','address','account']
hexes = list(set(string.hexdigits.lower()))

def salted_hash(d, salt=None):
    if not salt: salt = ''.join(np.random.choice(hexes,size=22))
    h = blake2b(digest_size=10)  
    if isinstance(salt, str):
        h.update(salt.encode())
    else:
        h.update(salt)
    for k in trisa_pii_set:
        v = d.get(k,'')
        if not v: raise ValueError('must know this info')
        s = v.translate(str.maketrans('','',string.punctuation)).lower()
        h.update(s.encode())
    return h.hexdigest(), salt

def gen_btc(user=None):
    hash160 = ''.join(np.random.choice(hexes, size=40))
    return vbtc.hex_to_b58check(hash160)
