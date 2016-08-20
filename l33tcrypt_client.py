#!/usr/bin/env python
# utf-8

import base64
import socket
import time
import string
import random
from threading import Thread, RLock

magic_word = 'l33tserver please'
LEN = 8096

def encrypt(msg, add_magic_word=True) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('l33tcrypt.vuln.icec.tf', 6001))

    buf = ''
    while not buf.startswith('Welcome to l33tserver where all your encryption needs are served.\n' + 
                             'Send me something to encrypt:\n') :
        buf += sock.recv(LEN)
    #print '[recvd]', buf

    if add_magic_word :
        to_send = magic_word + msg
    else:
        to_send = msg

    sock.sendall(base64.b64encode(to_send) + '\n')
    print '[sent]', base64.b64encode(to_send), ' - ', to_send

    buf = ''
    while not buf.startswith('Your l33tcrypted data:\n') :
        buf = sock.recv(len('Your l33tcrypted data:\n'))
    buf = sock.recv(LEN)

    sock.close()

    buf_dec = base64.b64decode(buf)    
    the_len = len(buf_dec)
    #print '[recvd]', buf, ' - ', the_len, ' - ', len(to_send) 

    return buf_dec

class ThreadEncrypt(Thread) :
    def __init__(self, msg, car, add_magic_words=True) :
        Thread.__init__(self)
        self.msg = msg
        self.car = car
        self.ciphered = None
        self.add_magic_words = add_magic_words


    def run(self) :
        self.ciphered = encrypt(self.msg, self.add_magic_words)
    
def padded_size(len_msg, block_size=16) :
    return len_msg + block_size - \
        ((len_msg + block_size) % block_size)


''' Calcul de la longueur du flag '''
m = ''
smallest_clear_len = len(magic_word) + len(m)

c = encrypt(m)

ciphered_len = len(c)
smallest_ciphered_len = ciphered_len

while ciphered_len == smallest_ciphered_len :
    m += 'a'
    c = encrypt(m)
    ciphered_len = len(c)

bytes_rem = len(magic_word) + len(m) - 1 - smallest_clear_len # remaining number of bytes in the smallest block
flag_len = smallest_ciphered_len - smallest_clear_len - bytes_rem
print
print 'flag_len: ', flag_len
print

''' Calcul de la taille du bloc '''
last_ciphered_len = ciphered_len
while ciphered_len == last_ciphered_len :
    m += 'a'
    c = encrypt(m)
    ciphered_len = len(c)
block_size = ciphered_len - last_ciphered_len
print
print 'block_size: ', block_size
print

"""
flag_len=50
block_size=16
"""

''' Cherchons le flag '''
payload = magic_word + 'a' * (padded_size(len(magic_word)) - len(magic_word)) + \
          'a' * block_size + \
          'a' * padded_size(flag_len)

print 'padded_size:', padded_size(flag_len)
print payload, '-', len(payload)

index = 1
found_suffix = ''
last_block = len(payload)/16

while index < flag_len :
    dico = {}
    dico2 = {}
    l_threads = []
    n_threads = 0

    for car in string.printable :
        clear = payload[ : len(payload) - index ] + found_suffix + car
        the_thread = ThreadEncrypt(clear, car, False)
        l_threads += [ the_thread ]
        the_thread.start()
        n_threads += 1

        if n_threads == 50 :
            for the_thread in l_threads :
                the_thread.join()
                ciphered = the_thread.ciphered
                block = ciphered[ (last_block - 1) * block_size : last_block * block_size ]
                dico[block] = the_thread.car
                dico2[the_thread.car] = block
            l_threads = []
            n_threads = 0

    for the_thread in l_threads :
        the_thread.join()
        ciphered = the_thread.ciphered
        block = ciphered[ (last_block - 1) * block_size : last_block * block_size ]
        dico[block] = the_thread.car
        dico2[the_thread.car] = block

    clear = payload[ : len(payload) - index ]
    ciphered = encrypt(clear, False)
    block = ciphered[ (last_block - 1) * block_size : last_block * block_size ]

    print "-->", "last_block:", last_block, "block index:", (last_block - 1) * block_size
    print "-->", base64.b64encode(block)
    print "--> c:", base64.b64encode(dico2['c'])
    print "--> found: '" + dico[block] + "'"
    print

    found_suffix += dico[block]

    print "*****************************"
    print "found:", found_suffix
    print "found:", found_suffix.encode('string_escape')
    print "*****************************"

    index += 1
