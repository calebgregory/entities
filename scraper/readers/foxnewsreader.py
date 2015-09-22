import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import sqlite3
import nltk

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

visitedLinks = []

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def foxNewsRSSVisit():
    try:
        page = 'http://feeds.foxnews.com/foxnews/latest?format=xml'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[2:]:
                if link in visitedLinks:
                    pass
                else:
                    visitedLinks.append(link)
                    print 'visiting: ', link
                    print '##################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>',linkSource)
                    for line in linesOfInterest:
                        nohtml = striphtml(line)
                        filteredLine = re.sub('&nbsp;|&quot;', '', nohtml)
                        print filteredLine
                        time.sleep(2)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)
foxNewsRSSVisit()
