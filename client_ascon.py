import socket
import threading
import select
import ctypes
import ascon_wrapper
import hashlib
import math
import random
import dh
import time


HOST = '10.0.2.15'
PORT = 1776


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Enter your nickname: ")


##################Key creation#####################
#Agreed upon numbers for Diffie-Hellman Key Exchange
p = (2**1536) - (2**1472) - 1 + (2**64) * ((int(2**1406 * 3)) + 741804)
g = 2

#UGV key generation
#This is client-dependent, make sure this is the right file for the
#Right machine
myprivate, mypublic = dh.generate_keys(p, g)

your_pubkey = 0
shared_key = 0


message_bytes = b''
key_bytes = b'' 
nonce_bytes = b''


def receive():
    while True:
        try:
            message = client.recv(1024)
            try:
                decode_message = message.decode('utf-8')
                if decode_message == 'NICK':
                    client.send(f"{nickname}:{mypublic}".encode('utf-8'))
                elif decode_message.startswith('Public key'):
                    mtosplit = decode_message.split(':')
                    your_pubkey_str = mtosplit[1]
                    your_pubkey = int(your_pubkey_str)
                    shared_key = dh.compute_shared(your_pubkey, myprivate, p)
                    write_thread = threading.Thread(target=write, args=(shared_key,))
                    write_thread.start()

                elif decode_message.startswith('Server:'):
                    print(decode_message)
            except UnicodeDecodeError:
                start_time = time.time()
                decrypt_bytes = b''
                decrypt_buffer = ctypes.create_string_buffer(129)
                uchar_decrypt = ctypes.cast(decrypt_buffer, ctypes.POINTER(ctypes.c_ubyte))

                incoming_bytes = b'' + message
                ibytes_size = len(incoming_bytes) + 1
                incoming_buffer = ctypes.create_string_buffer(ibytes_size)
                incoming_buffer.value = incoming_bytes
                uchar_incoming = ctypes.cast(incoming_buffer, ctypes.POINTER(ctypes.c_ubyte))

                shared_key_bytes = hex(shared_key)
                shared_key_bytes_str = str(shared_key_bytes[2:])

                key_bytes = b'' + shared_key_bytes_str.encode()
                kbytes_size = len(key_bytes) + 1
                key_buffer = ctypes.create_string_buffer(kbytes_size)
                key_buffer.value = key_bytes
                uchar_key = ctypes.cast(key_buffer, ctypes.POINTER(ctypes.c_ubyte))

                nonce_bytes = b'' + shared_key_bytes_str[:16].encode()
                nbytes_size = len(nonce_bytes) + 1
                nonce_buffer = ctypes.create_string_buffer(nbytes_size)
                nonce_buffer.value = nonce_bytes
                uchar_nonce = ctypes.cast(nonce_buffer, ctypes.POINTER(ctypes.c_ubyte))

                ascon_wrapper.decrypt_cipher(uchar_incoming, uchar_key, uchar_nonce, uchar_decrypt)

                print(decrypt_buffer.value.decode('utf-8'))

                end_time = time.time()
                decryption_time = end_time - start_time
                with open('logs.txt', 'a') as file:
                    file.write(f'dtime:{decryption_time}, len:{len(incoming_buffer.value.hex())}\n')

                continue

        except:
            print("An error occurred.")
            client.close()
            break




def write(shared_key):
    print("You can begin sending encrypted messages")
    while True:
        if(shared_key != 0):
            
            message = f'{nickname}: {input("")}'
            start_time = time.time()
            shared_key_bytes = hex(shared_key)
            shared_key_bytes_str = str(shared_key_bytes[2:])

            message_bytes = b"" + message.encode()
            mbytes_size = len(message_bytes) + 1
            message_buffer = ctypes.create_string_buffer(mbytes_size)
            message_buffer.value = message_bytes
            uchar_message = ctypes.cast(message_buffer, ctypes.POINTER(ctypes.c_ubyte))

            shared_key_bytes = hex(shared_key)
            shared_key_bytes_str = str(shared_key_bytes[2:])   

            key_bytes = b"" + shared_key_bytes_str.encode()
            kbytes_size = len(key_bytes) + 1
            key_buffer = ctypes.create_string_buffer(kbytes_size)
            key_buffer.value = key_bytes
            uchar_key = ctypes.cast(key_buffer, ctypes.POINTER(ctypes.c_ubyte))

            
            cipher_bytes = b""
            cipher_buffer = ctypes.create_string_buffer(135)
            uchar_cipher = ctypes.cast(cipher_buffer, ctypes.POINTER(ctypes.c_ubyte))

            nonce_bytes = b"" + shared_key_bytes_str[:16].encode()
            nbytes_size = len(nonce_bytes) + 1
            nonce_buffer = ctypes.create_string_buffer(nbytes_size)
            nonce_buffer.value = nonce_bytes
            uchar_nonce = ctypes.cast(nonce_buffer, ctypes.POINTER(ctypes.c_ubyte))

            ascon_wrapper.encrypt_message(uchar_message, uchar_key, uchar_nonce, uchar_cipher)

            client.send(cipher_buffer.value)

            end_time = time.time()
            encryption_time = end_time - start_time
            with open('logs.txt', 'a') as file:
                    file.write(f'etime:{encryption_time}, len:{len(cipher_buffer.value.hex())}\n')


receive_thread = threading.Thread(target=receive)
receive_thread.start()






