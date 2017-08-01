#!/usr/bin/env python
import sys
import crypt
import os

shadowfile = sys.argv[1]
wordlist = sys.argv[2]
uhs = "./uhs.txt"

cmdstring = "cat %s | tr ':$' ' ' | grep -v '!\|*' | cut -d ' ' -f 1,4,5 > ./uhs.txt" % (sys.argv[1])
os.system(cmdstring)

for line in open(uhs):
    uhsinfo = line.split()
    username = uhsinfo[0]
    salt = uhsinfo[1]
    passHash = uhsinfo[2]
    hashprefix = "$6$"

    for word in open(wordlist):
        calculatedHash = crypt.crypt(word.strip('\n'), hashprefix+salt)
	      if(calculatedHash.split('$')[3] == passHash):
            print(username+"'s password is :"+word.strip('\n'))
