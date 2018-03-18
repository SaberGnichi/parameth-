import sys
import argparse
import requests
from bs4 import BeautifulSoup
import random
from termcolor import colored

def reflectedinscriptcontext(content, value):
    reflected = False
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup.find_all('script'):
        script.encode('utf-8')
        if value in content:
            reflected = True
    return reflected

def getnames(content):
    names = []
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all('input'):
        try:
            name = tag.attrs['name']
            if len(name) > 0:
                names.append(name)
        except Exception:
            pass
    for tag in soup.find_all('form'):
        try:
            name = tag.attrs['name']
            if len(name) > 0:
                names.append(name)
        except Exception:
            pass
    if len(source) > 0:
        with open(source, 'r') as ins:
            for line in ins:
                line = line.strip()
                names.append(line)
    return names

def uniquearray(arr):
    rarr = []
    j = 0
    l = 0
    while j < len(arr):
        isnew = True
        i = 0
        element = arr[j]
        while i < l:
            if element == rarr[i]:
                isnew = False
            i += 1
        if isnew == True:
            rarr.append(element)
            l += 1
        j += 1
    return rarr

def randomstring(x):
    f = 'azertyuiopmlkjhgfdsqwxcvbn0123456789'
    j = 0
    r = ''
    while j < x:
        c = f[random.randint(0, len(f) - 1)]
        r += c
        j += 1
    return r
                            
def go():
    if ismulti == True:
        with open(file, 'r') as ins:
            for line in ins:
                line = line.strip()
                r = requests.get(line, headers=headers)
                names = getnames(r.content)
                names = uniquearray(names)
                j = 0
                cleanUrl = line
                while cleanUrl[len(cleanUrl) - 1] == '&' or cleanUrl[len(cleanUrl) - 1] == '?':
                    cleanUrl = cleanUrl[:-1]
                while j < len(names):
                    rstr = randomstring(10)
                    if '?' in cleanUrl:
                        char = '&'
                    else:
                        char = '?'
                    newUrl = cleanUrl + char + names[j] + '=' + rstr
                    rr1 = requests.get(newUrl, headers=headers)
                    if str(rr1.status_code) != '404':
                        if len(rr1.content) != len(r.content):
                            msg1 = '+ different length for ' + newUrl
                            print colored(msg1, 'yellow')
                            if rstr in rr1.content:
                                msg2 = '* ' + newUrl + ' ( the value of the get parameter ' + names[j] + ' reflected on the new content)'
                                print colored(msg2, 'blue')
                                if reflectedinscriptcontext(rr1.content, rstr) == True:
                                    msg = '- ' + newUrl + ' the value of the get parameter ' + names[j] + ' reflected on the script context'
                                    print colored(msg, 'red')
                    
                    data = {
                        names[j]: rstr
                    }
                    rr2 = requests.post(cleanUrl, headers=headers, data=data)
                    if str(rr2.status_code) != '404':
                        if len(rr2.content) != len(r.content):
                            msg3 = '+ different length for ' + cleanUrl + ' with post parameter ' + names[j]
                            print colored(msg3, 'yellow')
                            if rstr in rr2.content:
                                msg4 = '* ' + newUrl + ' ( the value of the post parameter ' + names[j] + ' reflected on the new content)'
                                print colored(msg4, 'blue')
                                if reflectedinscriptcontext(rr2.content, rstr) == True:
                                    msg = '- ' + newUrl + ' the value of the get parameter ' + names[j] + ' reflected on the script context'
                                    print colored(msg, 'red')
                    j += 1
    else:
        r = requests.get(url, headers=headers)
        names = getnames(r.content)
        names = uniquearray(names)
        j = 0
        cleanUrl = url
        while cleanUrl[len(cleanUrl) - 1] == '&' or cleanUrl[len(cleanUrl) - 1] == '?':
            cleanUrl = cleanUrl[:-1]
        while j < len(names):
            rstr = randomstring(10)
            if '?' in cleanUrl:
                char = '&'
            else:
                char = '?'
            newUrl = cleanUrl + char + names[j] + '=' + rstr
            rr1 = requests.get(newUrl, headers=headers)
            if str(rr1.status_code) != '404':
                if len(rr1.content) != len(r.content):
                    msg1 = '+ different length for ' + newUrl
                    print colored(msg1, 'yellow')
                    if rstr in rr1.content:
                        msg2 = '* ' + newUrl + ' ( the value of the get parameter ' + names[j] + ' reflected on the new content)'
                        print colored(msg2, 'blue')
            data = {
                names[j]: rstr
            }
            rr2 = requests.post(cleanUrl, headers=headers, data=data)
            if str(rr2.status_code) != '404':
                if len(rr2.content)!= len(r.content):
                    msg3 = '+ different length for ' + cleanUrl + ' with post parameter ' + names[j]
                    print colored(msg3, 'yellow')
                    if rstr in rr2.content:
                        msg4 = '* ' + newUrl + ' ( the value of the post parameter ' + names[j] + ' reflected on the new content)'
                        print colored(msg4, 'blue')
            j += 1
useragents = []
with open('user-agents.txt', 'r') as uas:
    for ua in uas:
        ua
headers = {
    'User-Agent': useragent
}
description = ''
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-f','--file', help='the file that contains urls', default='')
parser.add_argument('-u','--url', help='the url', default='')
parser.add_argument('-s','--source', help='the source file that contains common words to be used as params', default='')

args = vars(parser.parse_args())
file = args['file']
url = args['url']
source = args['source']
ismulti = False
if len(file) > 0:
    ismulti = True
try:
    go()
except KeyboardInterrupt:
    print colored('Terminated by the user', 'green')
