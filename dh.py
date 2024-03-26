import hashlib
import math
import random


def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def generate_keys(p, g):
    pk = random.randint(2, p-2)
    pubk = mod_exp(g, pk, p)
    return pk, pubk

def compute_shared(theirkey, mykey, p):
    return mod_exp(theirkey, mykey, p)

#step 1 agree on p and g

#p and g are from the RFC 3526 new Modular Exponential(MODP)
#groups for the Internet Key Exchange (IKE) protocol,
#documenting well known and used bit groups.
#p = (2**1536) - (2**1472) - 1 + (2**64) * ((int(2**1406 * 3)) + 741804)
#g = 2


#step 2 generate public and private keys
#private key will be kept private
#public key will be shared between parties

#UGV
#ugv_private, ugv_public = generate_keys(p, g)

#UAV
#uav_private, uav_public = generate_keys(p, g)


#calculate shared key by using your own private + received public
#use this shared key for encryption/decryption
#ugv_shared = compute_shared(uav_public, ugv_private, p)
#uav_shared = compute_shared(ugv_public, uav_private, p)


#ugv_shared_bytes = hex(ugv_shared)
#uav_shared_bytes = hex(uav_shared)

#ugv_shared_bytes_str = str(ugv_shared_bytes[2:])

#uav_shared_bytes_str = str(uav_shared_bytes[2:])

#print(ugv_shared_bytes_str)
#print(uav_shared_bytes_str)