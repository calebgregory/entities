import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import psycopg2
import nltk

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

def huffingtonRSSVisit():
    try:
        page = 'http://www.huffingtonpost.com/feeds/index.xml'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[1:]:
                linkIsVisited = isLinkVisited(link)
                if linkIsVisited is True:
                    pass
                else:
                    linkId = addLinkAndGetId(link, 'Huffington Post') # 2 : Huffington Post
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    for line in linesOfInterest:
                        processor(striphtml(line), linkId)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)
