import psycopg2
import unittest
import logging
from common.basic_operation import *
from triangle.tria import *

class TriangleTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1")
        self.youtube_tbl = "task7_youtube_edge"
        # self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")

    def tearDown(self):
        drop_if_exists(self.youtube_tbl, self.conn)

    def test_youtube(self):
        data_file = open('data/com-youtube.ungraph.txt')
        cur = self.conn.cursor()
        cur.execute("drop table if exists %s" % self.youtube_tbl)
        cur.execute("create table %s(from_id int, to_id int, value real DEFAULT 1)" % (self.youtube_tbl))
        cur.copy_from(data_file, self.youtube_tbl, columns=('from_id', 'to_id'))
        reverse_edge(self.youtube_tbl, conn)
        print "[com-youtube.ungraph.txt] loaded."
        r = count_triangle(self.youtube_tbl, self.conn)
        print "There are %s triangles in [com-youtube.ungraph.txt]." % r