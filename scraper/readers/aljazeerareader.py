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

def alJazeeraRSSVisit():
    try:
        page = 'http://america.aljazeera.com/content/ajam/articles.rss'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[1:]:
                time.sleep(1)
                if link in visitedLinks:
                    print 'link already visited'
                else:
                    visitedLinks.append(link)
                    print 'visiting: ', link
                    print '##################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    print "Content:"
                    for line in linesOfInterest:
                        filteredLine = re.sub(r'&nbsp;','',line)
                        print striphtml(filteredLine)
                    time.sleep(5)
        except Exception, e:
            print 'failed main loop of newYorkTimesRSSVisit'
            print str(e)
    except Exception, e:
        print 'failed main loop of newYorkTimesRSSVisit'
        print str(e)
alJazeeraRSSVisit()
