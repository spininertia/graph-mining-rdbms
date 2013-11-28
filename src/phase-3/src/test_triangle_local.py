import psycopg2
import unittest
import logging
from common.basic_operation import *
from triangle.tria import *

class LocalTriangleTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")

    def tearDown(self):
        pass

    def test_wikivote(self):
        """http://snap.stanford.edu/data/wiki-Vote.html"""
        data_file = "data/wiki-Vote.txt"
        gfile = "task7_wiki_vote"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        print "Wiki vote builded ..."
        reverse_matrix(gfile, self.conn)
        # count local triangle
        r = count_triangle(gfile, self.conn)
        drop_if_exists(gfile, self.conn)