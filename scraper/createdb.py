import psycopg2

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
