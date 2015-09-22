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

conn = sqlite3.connect('/Users/calebgregory/code/entities/scraper/knowledgebase.sqlite')
c = conn.cursor()

visitedLinks = []

def processor(data):
    try:
        tokens = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokens)
        namedEnt = nltk.ne_chunk(tagged, binary=True)

        entities = re.findall(r'NE\s(.*?)/', str(namedEnt))
        descriptives = re.findall(r'\(\'(\w*)\',\s\'JJ\w?\'', str(tagged))

        if len(entities) > 1:
            #multiEntities(data)
            # identifies either the main entities or splits that sentence
            # into parts that are about each entity
            pass
        elif len(entities) == 0:
            pass
            # relate descriptive words to the entity most recently discussed
            # e.g., 'former', 'latter' correspond to two things mentioned
        else:
            print 'Named: ',entities[0]
            print 'Descriptions: '
            for eachDesc in descriptives:
                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
                namedEntity = entities[0]
                relatedWord = eachDesc
                c.execute('INSERT INTO knowledgeBase (unix, datestamp, namedEntity, relatedWord) VALUES (?,?,?,?)',
                        (currentTime, dateStamp, namedEntity, relatedWord))
                conn.commit()

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
                if link in visitedLinks:
                    print 'link already visited'
                else:
                    visitedLinks.append(link)
                    print 'visiting: ', link
                    print '##################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    print 'Content:'
                    for line in linesOfInterest:
                        if '<img width' in line:
                            pass
                        elif '<a href=' in line:
                            pass
                        else:
                            processor(line)
        except Exception, e:
            print 'failed in 2nd loop of huffingtonRSSVisit'
            print str(e)
    except Exception, e:
        print 'failed main loop of huffingtonRSSVisit'
        print str(e)

def createDB():
    c.execute("CREATE TABLE IF NOT EXISTS knowledgeBase (unix TIMESTAMP, datestamp DATETIME, namedEntity VARCHAR(30), relatedWord VARCHAR(30))")
    conn.commit()

createDB()

while 1 < 2:
    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    huffingtonRSSVisit()
    print 'sleeping'
    print dateStamp
    time.sleep(900)
