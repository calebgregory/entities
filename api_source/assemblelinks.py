import psycopg2
import time
import datetime

postgres = """dbname='testdb' host='localhost'"""
postgres2 = """dbname='testdb2' host=localhost"""

def doesThisAlreadyExist(articleUrl):
    try:
        c2.execute("""
            SELECT * FROM linkswithsentiment
            WHERE url = '%s';
                """ % (str(articleUrl)))
        article = c2.fetchone()
        if article == None:
            return False
        else:
            return True
    except Exception, e:
        print 'failed in first layer of doesThisAlreadyExist'
        print str(e)

def sendValToNewDb(val):
    try:
        c2.execute("""
            INSERT INTO linkswithsentiment(created,url,value)
            VALUES ('%s', '%s', '%s');
                """ % (str(val[0]), str(val[1]), str(val[2])))
        conn2.commit()
    except Exception, e:
        print 'failed in first layer of sendValToNewDb'
        print str(e)

def getSentimentsValsForArticle():
    try:
        c.execute("""
        SELECT VL.created, VL.url, SUM(SV.value)
        FROM visitedlinks AS VL
        INNER JOIN associations AS A
        ON A.linkid = VL.linkid
        INNER JOIN sentimentval AS SV
        ON SV.word = A.word
        GROUP BY VL.url, VL.created
        ORDER BY VL.created desc;
                """)
        sent_vals = c.fetchall()
        for val in sent_vals:
            alreadyExists = doesThisAlreadyExist(val[1])
            if alreadyExists:
                pass
            else:
                sendValToNewDb(val)
    except Exception, e:
        print 'failed in first layer of getSentimentsValsForArticle'
        print str(e)

def insertIntoSentimentBySourceDB(source, atTime):
    try:
        average = source[2] / source[3] # value / number of articles per source
        c2.execute("""
            INSERT INTO sentimentbysource(created, sourceid, name, average)
            VALUES ('%s', '%s', '%s', '%s');
        """ % (atTime, str(source[0]), str(source[1]), str(average)))
        conn2.commit()

    except Exception, e:
        print 'failed in first layer of insertIntoSentimentBySourceDB'
        print str(e)

def getSentimentValsByNewsSource():
    try:
        c.execute("""
            SELECT S.sourceid, S.name, SUM(SV.value), COUNT(vl.linkid)
            FROM sources AS S
            INNER JOIN visitedLinks as VL
            ON VL.sourceid = S.sourceid
            INNER JOIN associations AS A
            ON A.linkid = VL.linkid
            INNER JOIN sentimentval AS SV
            ON SV.word = A.word
            GROUP BY S.sourceid, S.name
            ORDER BY SUM(SV.value) DESC;
                """)
        sources_with_val = c.fetchall()
        currentTime = time.time()
        dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
        for source in sources_with_val:
            insertIntoSentimentBySourceDB(source,dateStamp)
    except Exception, e:
        print 'failed in first layer of getSentimentsValsByNewsSource'
        print str(e)

conn2 = psycopg2.connect(postgres2)
c2 = conn2.cursor()

c2.execute("""CREATE TABLE IF NOT EXISTS linkswithsentiment (created timestamp, url TEXT, value REAL);""")
c2.execute("""CREATE TABLE IF NOT EXISTS sentimentbysource (created timestamp, sourceid INT, name varchar(40), average REAL);""")

conn2.commit()
conn2.close()

currentTime = time.time()
dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
print '> Boot successful', dateStamp


while (1 < 2):
    conn = psycopg2.connect(postgres)
    c = conn.cursor()

    conn2 = psycopg2.connect(postgres2)
    c2 = conn2.cursor()

    getSentimentsValsForArticle()
    getSentimentValsByNewsSource()

    conn.close()
    conn2.close()

    currentTime = time.time()
    dateStamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    print dateStamp, '[ Successfully added more links ]'

    time.sleep(900)
