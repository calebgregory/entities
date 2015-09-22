import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime
import sqlite3

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

conn = sqlite3.connect('/Users/calebgregory/code/entities/scraper/knowledgebase.sqlite')
conn.text_factory = str
c = conn.cursor()

def createDB():
    c.execute("CREATE TABLE IF NOT EXISTS wordVals (word TEXT, value REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS doneSyns (word TEXT, synonym TEXT)")

# good, bad, neutral; 1, -1, 0
startingWord = 'bad'
startingWordVal = -1

synArray = []

def main():
    try:
        page = 'http://thesaurus.com/browse/'+startingWord+'?s=t'
        sourceCode = opener.open(page).read()
        try:
            synoNym = sourceCode.split('<section class="container-info antonyms">')[0]
            synoNym = synoNym.split('class="synonyms"')[1]
            synonymList = re.findall(r'<span class="text">(.*?)</span>', synoNym)
            for syn in synonymList:
                query = "SELECT * FROM wordVals WHERE word =?"
                c.execute(query, [(syn)])
                data = c.fetchone()

                if data is None:
                    print 'not here yet, let\'s add it'
                    c.execute("INSERT INTO wordVals (word, value) VALUES (?,?)",
                            (syn, startingWordVal))
                    conn.commit()

                    subPage = 'http://thesaurus.com/browse/'+syn+'?s=t'
                    subSourceCode = opener.open(subPage).read()
                    subSynoNym = subSourceCode.split('<section class="container-info antonyms">')[0]
                    subSynoNym = subSynoNym.split('class="synonyms"')[1]
                    subSynonymList = re.findall(r'<span class="text">(.*?)</span>', subSynoNym)
                    for subsyn in subSynonymList:
                        query = "SELECT * FROM wordVals WHERE word =?"
                        c.execute(query, [(subsyn)])
                        data = c.fetchone()

                        if data is None:
                            print 'not here yet, let\'s add it'
                            c.execute("INSERT INTO wordVals (word, value) VALUES (?,?)",
                                    (subsyn, startingWordVal))
                            conn.commit()
                            subsubPage = 'http://thesaurus.com/browse/'+subsyn+'?s=t'
                            subsubSourceCode = opener.open(subsubPage).read()
                            subsubSynoNym = subsubSourceCode.split('<section class="container-info antonyms">')[0]
                            subsubSynoNym = subsubSynoNym.split('class="synonyms"')[1]
                            subsubSynonymList = re.findall(r'<span class="text">(.*?)</span>', subsubSynoNym)
                            for subsubsyn in subsubSynonymList:
                                query = "SELECT * FROM wordVals WHERE word =?"
                                c.execute(query, [(subsubsyn)])
                                data = c.fetchone()

                                if data is None:
                                    print 'not here yet, let\'s add it'
                                    c.execute("INSERT INTO wordVals (word, value) VALUES (?,?)",
                                            (subsubsyn, startingWordVal))
                                    conn.commit()
                                else:
                                    print 'word already here!'
                        else:
                            print 'word already here!'
                else:
                    print 'word already here!'
        except Exception, e:
            print 'failed second try in main'
            print str(e)
    except Exception, e:
        print 'failed in main loop'
        print str(e)

createDB()
main()

c.execute("INSERT INTO doneSyns (word) VALUES (?)",
        [(startingWord)])
conn.commit()

