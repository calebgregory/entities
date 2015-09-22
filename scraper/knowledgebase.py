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

#conn = psycopg2.connect('/Users/calebgregory/code/entities/scraper/knowledgebase.sqlite')
#c = conn.cursor()

visitedLinks = []

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def processor(data, sourceId):
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

                time.sleep(1)

            else:
                print 'we don\'t want', tag
        #namedEnt = nltk.ne_chunk(tagged, binary=True)

        #entities = re.findall(r'NE\s(.*?)/', str(namedEnt))
        #descriptives = re.findall(r'\(\'(\w*)\',\s\'JJ\w?\'', str(tagged))

        #if len(entities) > 1:
            ##multiEntities(data)
            ## identifies either the main entities or splits that sentence
            #pass
            ## into parts that are about each entity
        #elif len(entities) == 0:
            #pass
            ## relate descriptive words to the entity most recently discussed
            ## e.g., 'former', 'latter' correspond to two things mentioned
        #else:
            #print 'Named: ', str.lower(entities[0])
            #print 'Descriptions: '
            #for eachDesc in descriptives:
                #print '      >', str.lower(eachDesc)
                ##currentTime = time.time()
                ##namedEntity = entities[0]
                ##c.execute("""INSERT INTO associations (entity, descriptor, created, source) VALUES (%s,%s,%s,%s,%s)""",
                        ##(namedEntity, eachDesc, currentTime, sourceId))
                ##conn.commit()

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
                        processor(striphtml(line), 0)
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
                if 'feedsportal' in link:
                    pass
                elif link in visitedLinks:
                    print 'link already visited'
                else:
                    visitedLinks.append(link)
                    print 'visiting: ', link
                    print '##################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p class="story-body-text.*?itemprop="articleBody".*?>(.*?)</p>', str(linkSource))
                    print "Content:"
                    for line in linesOfInterest:
                        processor(striphtml(line), 1)
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
