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
        c.execute("""INSERT INTO visitedlinks (url, created, sourceid) VALUES ('%s', '%s', '%s') RETURNING linkid;""" %
                (str(link), datestamp, str(sourceid)))
        linkid = c.fetchone()[0]
        conn.commit()
        return linkid
    except Exception, e:
        print 'failed in addLink'
        print str(e)

def processor(data, linkId):
    try:
        filteredData = re.sub('&nbsp;|&quot;', '', data)
        tokens = nltk.word_tokenize(filteredData)
        tagged = nltk.pos_tag(tokens)

        currentTime = time.time()
        datestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')

        tagsWeWant = ['JJ', 'JJR', 'JJS',
                'NN', 'NNS',
                'PRP', 'PRPS',
                'RB', 'RBR', 'RBS',
                'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'VBT']

        for tag in tagged:
            if tag[1] in tagsWeWant:
                word = re.sub(r'\'','',tag[0].lower())
                pos = tag[1]
                c.execute("""INSERT INTO associations (created, word, linkid, pos) VALUES ('%s', '%s', '%s', '%s')""" %
                        (datestamp, str(word), str(linkId), str(pos)))
                conn.commit()
            else:
                pass

    except Exception, e:
        if "'ascii' codec" not in str(e):
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
            print str(e)
    except Exception, e:
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
            print str(e)
    except Exception, e:
        print str(e)

def foxNewsRSSVisit():
    try:
        page = 'http://feeds.foxnews.com/foxnews/latest?format=xml'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[2:]:
                linkIsVisited = isLinkVisited(link)
                if linkIsVisited is True:
                    pass
                else:
                    linkId = addLinkAndGetId(link, 'Fox News')
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>',linkSource)
                    for line in linesOfInterest:
                        processor(striphtml(line), linkId)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

def nprRSSVisit():
    try:
        page = 'http://www.npr.org/rss/rss.php?id=1001'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[2:]:
                linkIsVisited = isLinkVisited(link)
                if linkIsVisited is True:
                    pass
                else:
                    linkId = addLinkAndGetId(link, 'NPR')
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    for line in linesOfInterest:
                        processor(striphtml(line), linkId)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

def cnnRSSVisit():
    try:
        page = 'http://rss.cnn.com/rss/cnn_topstories.rss'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[2:]:
                linkIsVisited = isLinkVisited(link)
                if linkIsVisited is True:
                    pass
                elif 'feedsportal' in link:
                    pass
                else:
                    linkId = addLinkAndGetId(link, 'CNN')
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p class="zn-body__paragraph">(.*?)</p>', str(linkSource))
                    for line in linesOfInterest:
                        processor(striphtml(line), linkId)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

def alJazeeraRSSVisit():
    try:
        page = 'http://america.aljazeera.com/content/ajam/articles.rss'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links[1:]:
                linkIsVisited = isLinkVisited(link)
                if linkIsVisited is True:
                    pass
                else:
                    linkId = addLinkAndGetId(link, 'Al Jazeera')
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    for line in linesOfInterest:
                        processor(striphtml(line), linkId)
        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

postgres = """dbname='testdb' host='localhost'"""

conn = psycopg2.connect(postgres)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS sources (sourceid SERIAL PRIMARY KEY NOT NULL, name VARCHAR(40));""")
c.execute("""INSERT INTO sources(name) VALUES ('Huffington Post');""")
c.execute("""INSERT INTO sources(name) VALUES ('New York Times');""")
c.execute("""INSERT INTO sources(name) VALUES ('Fox News');""")
c.execute("""INSERT INTO sources(name) VALUES ('CNN');""")
c.execute("""INSERT INTO sources(name) VALUES ('NPR');""")
c.execute("""INSERT INTO sources(name) VALUES ('Al Jazeera');""")
c.execute("""CREATE TABLE IF NOT EXISTS visitedlinks (linkid SERIAL PRIMARY KEY NOT NULL, created TIMESTAMP, url TEXT, sourceid INT REFERENCES sources);""")
c.execute("""CREATE TABLE IF NOT EXISTS sentimentval (id SERIAL NOT NULL, word TEXT, value REAL);""")
c.execute("""CREATE TABLE IF NOT EXISTS associations (created TIMESTAMP, word TEXT, linkid INT REFERENCES visitedlinks, pos VARCHAR(5));""")
conn.commit()
conn.close()

currentTime = time.time()
dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
print dateStamp, '> Successful boot'

while 1 < 2:

    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    huffingtonRSSVisit()
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, 'Huffington Post'
    time.sleep(180)

    conn.close()

    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    newYorkTimesRSSVisit()
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, 'New York Times'
    time.sleep(180)

    conn.close()

    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    foxNewsRSSVisit()
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, 'Fox News'
    time.sleep(180)

    conn.close()

    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    nprRSSVisit()
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, 'NPR'
    time.sleep(180)

    conn.close()

    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    cnnRSSVisit()
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, 'CNN'
    time.sleep(180)

    conn.close()

    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    alJazeeraRSSVisit()
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, 'Al Jazeera'
    time.sleep(180)

    conn.close()
