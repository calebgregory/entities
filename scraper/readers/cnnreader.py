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

def cnnRSSVisit():
    try:
        page = 'http://rss.cnn.com/rss/cnn_topstories.rss'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[2:]:
                if 'feedsportal' in link:
                    pass
                elif link in visitedLinks:
                    print 'link already visited'
                else:
                    visitedLinks.append(link)
                    print 'visiting: ', link
                    print '##################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p class="zn-body__paragraph">(.*?)</p>', str(linkSource))
                    print "Content:"
                    for line in linesOfInterest:
                        print striphtml(line)
                        time.sleep(1)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

cnnRSSVisit()
