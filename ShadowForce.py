#!/usr/bin/env python
import sys
import crypt
import os
import base64
import argparse

class colors:
    PURPLE = '\033[95m'
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
def main(args):

    rows, columns = os.popen('stty size', 'r').read().split()
    banner = base64.b64decode('ICBfX198ICB8ICAgICAgICAgICAgICAgfCAgICAgICAgICAgICAgICAKXF9fXyBcICBfXyBcICAgX2AgfCAgX2AgfCAgXyBcXCBcICBcICAgLyAKICAgICAgfCB8IHwgfCAoICAgfCAoICAgfCAoICAgfFwgXCAgXCAvICAKX19fX18vIF98IHxffFxfXyxffFxfXyxffFxfX18vICBcXy9cXy8gICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICBfX19ffCAgICAgICAgICAgICAgICAgICAKICB8ICAgIF8gXCAgIF9ffCBfX3wgIF8gXCAKICBfX3wgKCAgIHwgfCAgICggICAgIF9fLyAKIF98ICBcX19fLyBffCAgXF9fX3xcX19ffA==')
    shadowfile = args.shadow
    wordlist = args.wordlist
    uhs = "./uhs.txt"
    cmdstring = "cat %s | tr ':$' ' ' | grep -v '!\|*' | cut -d ' ' -f 1,4,5 > ./uhs.txt" % (shadowfile)
    
    print(colors.PURPLE+banner.decode('ascii')+"\n"+colors.ENDC)
    os.system(cmdstring)
    finishedUsers = 0
    with open(uhs) as fd:
        totalUsers = sum(1 for _ in fd)
    fd.close()

    with open(uhs) as fd:
        totalWords = sum(1 for _ in fd)
    fd.close()

    cracked = []
    failed = []
    for line in open(uhs):
        finishedUsers += 1
        comp = "%0.1f" % ((finishedUsers / float(totalUsers))*100)
        if(comp == ("%0.1f" % float(100))):
            sys.stdout.write("\r%s%s complete%s" % (colors.SUCCESS, comp, colors.ENDC))
        else:
            sys.stdout.write("\r%s%s complete%s" % (colors.FAIL, comp, colors.ENDC))
        sys.stdout.flush()
        uhsinfo = line.split()
        username = uhsinfo[0]
        salt = uhsinfo[1]
        passHash = uhsinfo[2]
        hashprefix = "$6$"

        currentWord = 0
        for word in open(wordlist):
            currentWord += 1
            calculatedHash = crypt.crypt(word.strip('\n'), hashprefix+salt)
            if(calculatedHash.split('$')[3] == passHash):
                cracked.append("USERNAME: '"+username+"' PASSWORD: '"+colors.SUCCESS+word.strip('\n')+"'"+colors.ENDC)
            elif(currentWord == totalWords):
                failed.append(username)

    os.system("rm ./uhs.txt")
    print("\n")
    for x in cracked:
        print(x).strip("\n")
    print("\nFAILED to match a HASH for users:")
    for x in failed:
        print(colors.FAIL+x+colors.ENDC).strip("\n")

def parse_args():
    argParse = argparse.ArgumentParser(description='Brute force SHA512 shadow file')
    requiredArgs = argParse.add_argument_group('Required arguments')
    requiredArgs.add_argument('-s', dest="shadow", help="Shadow File", required=True)
    requiredArgs.add_argument('-w', dest="wordlist", help="Wordlist File", required=True)
    return argParse.parse_args()

if __name__ == "__main__":
    main(parse_args())
