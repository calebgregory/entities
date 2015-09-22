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

postgres = """dbname='testdb' host='localhost'"""
conn = psycopg2.connect(postgres)
c = conn.cursor()

visitedLinks = []

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

# called from
def isLinkVisited(link):
    try:
        c.execute("""SELECT url FROM visitedLinks WHERE url = '%s';""" % (str(link)))
        article = c.fetchone()
        if article is None:
            return False
        else:
            return True
    except Exception, e:
        print 'failed in isLinkVisited'
        print str(e)

def addLinkAndGetId(link, sourceName):
    try:
        currentTime = time.time()
        datestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
        c.execute("""SELECT sourceid FROM sources WHERE name = '%s';""" % (str(sourceName)))
        sourceid = c.fetchone()[0]
        c.execute("""INSERT INTO visitedlinks (url, created, sourceid) VALUES ('%s', now(), '%s') RETURNING linkid;""" %
                (str(link), str(sourceid)))
        linkid = c.fetchone()[0]
        conn.commit()
        return linkid
    except Exception, e:
        print 'failed in addLink'
        print str(e)

def processor(data, linkId):
    try:
        tokens = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokens)

        tagsWeWant = ['JJ', 'JJR', 'JJS',
                'NN', 'NNS',
                'PRP', 'PRPS',
                'RB', 'RBR', 'RBS',
                'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'VBT']
        for tag in tagged:
            if tag[1] in tagsWeWant:
                currentTime = time.time()
                datestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
                word = re.sub(r'\'','',tag[0].lower())
                pos = tag[1]
                c.execute("""INSERT INTO associations (created, word, linkid, pos) VALUES (now(), '%s', '%s', '%s')""" %
                        (str(word), str(linkId), str(pos)))
                conn.commit()
            else:
                pass

    except Exception, e:
        print 'failed in the first try of processor'
        print str(e)


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
            print 'failed in 2nd loop of huffingtonRSSVisit'
            print str(e)
    except Exception, e:
        print 'failed main loop of huffingtonRSSVisit'
        print str(e)

def newYorkTimesRSSVisit():
    try:
        page = 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'href="(.*?)"', sourceCode)
            for link in links[1:]:
                linkIsVisited = isLinkVisited(link)
                if linkIsVisited is True:
                    pass
                elif 'feedsportal' in link:
                    pass
                else:
                    linkId = addLinkAndGetId(link, 'New York Times')
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p class="story-body-text.*?itemprop="articleBody".*?>(.*?)</p>', str(linkSource))
                    for line in linesOfInterest:
                        processor(striphtml(line), linkId)
        except Exception, e:
            print 'failed main loop of newYorkTimesRSSVisit'
            print str(e)
    except Exception, e:
        print 'failed main loop of newYorkTimesRSSVisit'
        print str(e)

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
                        processor(filteredLine, 2)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

while 1 < 2:
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    huffingtonRSSVisit()
    print 'sleeping'
    print dateStamp
    time.sleep(15)
    newYorkTimesRSSVisit()
    print 'sleeping'
    print dateStamp
    time.sleep(15)
    foxNewsRSSVisit()
    print 'sleeping'
    print dateStamp
    time.sleep(15)
