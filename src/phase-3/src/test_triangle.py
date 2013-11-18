import sys
import psycopg2
from common.basic_operation import *
from triangle.tria import *

def test_dummy(conn):
    v = 'v'     
    cur = conn.cursor()    
    cur.execute("drop table if exists %s" % v)
    cur.execute("create table %s(from_id int, to_id int, value real)" % (v))
    f = open("data/matrix_data.txt")
    data = [line.strip().split(" ") for line in f]
    for i in range(len(data)):
        for j in range(len(data)):
            cur.execute("insert into %s values (%s, %s, %s)" % (v, i, j, data[i][j]))
    count_triangle(v, conn)

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_dummy(conn)    