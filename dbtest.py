import psycopg2


conn = psycopg2.connect()

try:
    conn = psycopg2.connect("dbname='chomper' user='django' host='localhost' password='gismogt'")
    print conn
except:
    print "I am unable to connect to the database"
    
    