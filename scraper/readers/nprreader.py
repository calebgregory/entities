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

def nprRSSVisit():
    try:
        page = 'http://www.npr.org/rss/rss.php?id=1001'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[2:]:
                if link in visitedLinks:
                    skip
                else:
                    visitedLinks.append(link)
                    print 'visiting: ', link
                    print '##################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    print "Content:"
                    for line in linesOfInterest:
                        print striphtml(line)
                        time.sleep(1)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

nprRSSVisit()
