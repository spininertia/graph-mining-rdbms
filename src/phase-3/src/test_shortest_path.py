import sys
import time
import psycopg2
import unittest
from common.basic_operation import *
from spath.dijkstra import *
from graph_generator import *

class ShortestPathTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1")    
        # self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")    

    def tearDown(self):
        pass

    @unittest.skip("")
    def test_dummydata(self):
        cur = self.conn.cursor()
        gname = "spath_graph"
        graph = [['1', '2', '1.0'], \
                 ['2', '3', '1.0'], \
                 ['1', '3', '1.0'], \
                 ['3', '4', '0.5'], \
                 ['3', '6', '1.6'], \
                 ['2', '6', '0.3']]
        drop_if_exists(gname, self.conn)
        cur.execute("create table %s (from_id int, to_id int, value real)" % gname)
        for edge in graph:
            cur.execute("insert into %s values (%s, %s, %s)" % (gname, edge[0], edge[1], edge[2]))
        dijkstra("1", gname, "spath_result", "spath", self.conn)
        cur = self.conn.cursor()
        cur.execute("select * from spath_result")
        print "Shortest Path result"
        for r in cur.fetchall():
            print r

    def test_runtime(self):
        cur = self.conn.cursor()
        gname = "spath_graph"
        generate_directed_graph(gname, 10000, self.conn)
        dijkstra("0", gname, "spath_result", "spath", self.conn)
        cur = self.conn.cursor()
        cur.execute("select * from spath_result")
        print "Shortest Path result"