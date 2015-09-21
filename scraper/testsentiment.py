from __future__ import division
import sqlite3
import time

conn = sqlite3.connect('/Users/calebgregory/code/entities/scraper/knowledgebase.sqlite')
c = conn.cursor()

negativeWords = []
positiveWords = []

sql = "SELECT * FROM wordVals WHERE value =?"

def loadWordArrays():
    for negRow in c.execute(sql, [(-1.0)]):
        negativeWords.append(negRow[0])
    print 'neg words loaded'

    for posRow in c.execute(sql, [(1.0)]):
        positiveWords.append(posRow[0])
    print 'pos words loaded'

def testPositiveSentiment():
    readFile = open('/Users/calebgregory/code/entities/scraper/<positive-reviews>.txt', 'r').read()
    splitRead = readFile.split('\n')
    totalExamples = len(splitRead)
    posExamplesFound = 0

    for eachPosExample in splitRead:
        sentCounter = 0
        for eachPosWord in positiveWords:
            if eachPosWord in eachPosExample:
                sentCounter += 1
        for eachNegWord in negativeWords:
            if eachNegWord in eachPosExample:
                sentCounter -= 1

        if sentCounter > 0:
            posExamplesFound += 1
    print ''
    print '_____________________________'
    print ' Positive sentiment accuracy:'
    print '   found examples:', posExamplesFound
    print '   out of:', totalExamples
    print ' positive accuracy:', posExamplesFound/totalExamples*100

def testNegativeSentiment():
    readFile = open('/Users/calebgregory/code/entities/scraper/<negative-reviews>.txt', 'r').read()
    splitRead = readFile.split('\n')
    totalExamples = len(splitRead)
    negExamplesFound = 0

    for eachNegExample in splitRead:
        sentCounter = 0
        for eachPosWord in positiveWords:
            if eachPosWord in eachNegExample:
                sentCounter += 1
        for eachNegWord in negativeWords:
            if eachNegWord in eachNegExample:
                sentCounter -= 1

        if sentCounter < 0:
            negExamplesFound += 1
    print ''
    print '_____________________________'
    print ' Negative sentiment accuracy:'
    print '   found examples:', negExamplesFound
    print '   out of:', totalExamples
    print ' negative accuracy:', negExamplesFound/totalExamples*100

loadWordArrays()
testSentiment()
