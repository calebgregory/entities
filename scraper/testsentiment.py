from __future__ import division
import psycopg2
import os
import time

negativeWords = []
positiveWords = []

sql = """SELECT word FROM sentimentval WHERE value = '%s'"""

#
#
#       download dataset at:
#       http://ai.stanford.edu/~amaas/data/sentiment/
#
#
#

def loadWordArrays():
    c.execute("""SELECT * FROM sentimentval WHERE value = '-1';""")
    allNegRows = c.fetchall()
    for negRow in allNegRows:
        negativeWords.append(negRow[1])
    print 'neg words loaded: >> total:', len(negativeWords)

    c.execute("""SELECT * FROM sentimentval WHERE value = '1';""")
    allPosRows = c.fetchall()
    for posRow in allPosRows:
        positiveWords.append(posRow[1])
    print 'pos words loaded: >> total:', len(positiveWords)

def testPositiveSentiment():
    pathToDir = '/Users/calebgregory/code/entities/scraper/pos'
    examples = os.listdir(pathToDir)

    totalExamples = len(examples)
    posExamplesFound = 0

    for filename in examples:
        readFile = open(os.path.join(pathToDir,filename), 'r').read()
        sentCounter = 0
        for eachPosWord in positiveWords:
            if eachPosWord in readFile:
                sentCounter += 1.475
        for eachNegWord in negativeWords:
            if eachNegWord in readFile:
                sentCounter -= 1

        if sentCounter > 0:
            posExamplesFound += 1

    print ''
    print '_____________________________'
    print ' Positive sentiment accuracy:'
    print '   found examples:', posExamplesFound
    print '   out of:', totalExamples
    print '   from all files in:', pathToDir
    print ' positive accuracy:', posExamplesFound/totalExamples*100

def testNegativeSentiment():

    pathToDir = '/Users/calebgregory/code/entities/scraper/neg'
    examples = os.listdir(pathToDir)

    negExamplesFound = 0
    totalExamples = len(examples)

    for filename in examples:
        readFile = open(os.path.join(pathToDir,filename), 'r').read()
        sentCounter = 0
        for eachPosWord in positiveWords:
            if eachPosWord in readFile:
                sentCounter += 1.475
        for eachNegWord in negativeWords:
            if eachNegWord in readFile:
                sentCounter -= 1

        if sentCounter < 0:
            negExamplesFound += 1

    print ''
    print '_____________________________'
    print ' Negative sentiment accuracy:'
    print '   found examples:', negExamplesFound
    print '   out of:', totalExamples
    print '   from all files in:', pathToDir
    print ' negative accuracy:', negExamplesFound/totalExamples*100

conn = psycopg2.connect("""dbname='testdb' host='localhost'""")
c = conn.cursor()

loadWordArrays()

conn.close()

testPositiveSentiment()
testNegativeSentiment()
