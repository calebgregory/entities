#!/usr/bin/env python

import psycopg2

postgres = """dbname='sentimentdb' user='preachypreach' host='<endpoint>' password='<password>'"""

words = []

def addPosiWords():
    posFile = open('/Users/calebgregory/code/entities/scraper/opinion-lexicon-English/positive-words.txt','r').read()
    splitRead = posFile.split('\n')
    for posiWord in splitRead:
        if posiWord == '' or ';' in posiWord:
            pass
        else:
            words.append({'word': posiWord, 'value': 1})

def addNegWords():
    negFile = open('/Users/calebgregory/code/entities/scraper/opinion-lexicon-English/negative-words.txt','r').read()
    splitRead = negFile.split('\n')
    for negWord in splitRead:
        if negWord == '' or ';' in negWord:
            pass
        else:
            words.append({'word': negWord, 'value': -1})

def addWordsToDb():
    try:
        conn = psycopg2.connect(postgres)
        print "connection successful"
    except Exception, e:
        print str(e)
        print "unable to connect to database"

    c = conn.cursor()

    for word in words:
        try:
            c.execute("""INSERT INTO sentimentval(word, value) VALUES ('%s', %s);""" % (word['word'], str(word['value'])))
        except Exception, e:
            print word
            print str(e)
    conn.commit()
    print "inserted values into table"
    c.execute("""SELECT * FROM sentimentval LIMIT 25;""")
    rows = c.fetchall()
    print "rows:"
    for row in rows:
        print '  ', row
    conn.close()

addPosiWords()
addNegWords()
addWordsToDb()
print "all done"
