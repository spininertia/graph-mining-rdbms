import sys
import psycopg2
from common.basic_operation import *
from triangle.tria import *

def test_dummy(conn):
    v = 'v'     
    cur = conn.cursor()    
    cur.execute("drop table if exists %s" % v)
    cur.execute("create table %s(from_id int, to_id int, value real DEFAULT 1)" % (v))
    f = open("data/p2p-Gnutella08.txt")
    cur.copy_from(f, v, columns=('from_id', 'to_id'))
    print "data loaded"
    count_triangle(v, conn)

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_dummy(conn)    