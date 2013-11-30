import sys
import time
import psycopg2
import unittest
from mst.mst import *
from graph_generator import *
class MinimumSpanningTreeTest(unittest.TestCase):
  def setUp(self):
    self.conn = psycopg2.connect(database="mydb", host="127.0.0.1")    

  def tearDown(self):
    pass
    
  def test_runtime(self):
    cur = self.conn.cursor()
    gname = "mst_graph"
    generate_undirected_graph(gname, 500, self.conn)
    print "graph builded"
    mst(self.conn, gname, gname)		
