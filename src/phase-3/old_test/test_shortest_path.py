import sys
import time
import psycopg2
from common.basic_operation import *
from spath.dijkstra import *

def time_it(fn):
    def wrapped(*args):
        start = time.time()
        fn(*args)
        used = time.time() - start
        print "Used %s seconds. " % used
    return wrapped

@time_it
def test_dummy(conn):
    cur = conn.cursor()
    gname = "spath_graph"
    graph = [['1', '2', '1.0'], ['2', '3', '1.0'], ['1', '3', '1.0']]
    drop_if_exists(gname, conn)
    cur.execute("create table %s (from_id int, to_id int, value real)" % gname)
    for edge in graph:
        cur.execute("insert into %s values (%s, %s, %s)" % (gname, edge[0], edge[1], edge[2]))
    dijkstra("1", gname, "spath_result", "spath", conn)


if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_dummy(conn)
