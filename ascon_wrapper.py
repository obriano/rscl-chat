import ctypes

# Load the shared library
lib = ctypes.CDLL("./asconctypes.so")

lib.encrypt.argtypes = [
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte)
]
lib.encrypt.restype = ctypes.c_int



lib.decrypt.argtypes = [
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
]
lib.decrypt.restype = ctypes.c_int


def encrypt_message(message, key, nonce, cipher):
    ret = lib.encrypt(
        message,
        key,
        nonce,
        cipher
    )


def decrypt_cipher(cipher, key, nonce, decrypted):
    ret = lib.decrypt(
        cipher,
        key,
        nonce,
        decrypted
    )