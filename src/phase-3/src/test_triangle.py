import psycopg2
import unittest
import logging
from common.basic_operation import *
from triangle.tria import *

class TriangleTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")

    def tearDown(self):
        pass

    def test_youtube(self):
        data_file = "data/com-youtube.ungraph.txt"
        gfile = "task7_youtube_graph"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        print "Youtube graph builded ..."
        reverse_matrix(gfile, self.conn)
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles in [com-youtube.ungraph.txt]." % r
        drop_if_exists(gfile, self.conn)

    @unittest.skip("")
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
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles." % r
        drop_if_exists(gfile, self.conn)

    @unittest.skip("")
    def test_enron_email(self):
        """http://snap.stanford.edu/data/email-Enron.html"""
        data_file = "data/email-Enron.txt"
        gfile = "task7_enron_email"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        print "Enron email builded ..."
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles." % r
        drop_if_exists(gfile, self.conn)

    @unittest.skip("")
    def test_slashdot0902(self):
        """http://snap.stanford.edu/data/soc-Slashdot0902.html"""
        data_file = "data/soc-Slashdot0902.txt"
        gfile = "task7_slashdot0902"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        print "Slashdot 0902 builded ..."
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles." % r
        drop_if_exists(gfile, self.conn)

    @unittest.skip("")
    def test_amazon_purchase(self):
        """http://snap.stanford.edu/data/com-Amazon.html"""
        data_file = "data/com-amazon.ungraph.txt"
        gfile = "task7_amazon_purchase"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        reverse_matrix(gfile, self.conn)
        print "Amazon builded ..."
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles." % r
        drop_if_exists(gfile, self.conn)

    @unittest.skip("")
    def test_web_stanford(self):
        """http://snap.stanford.edu/data/web-Stanford.html"""
        data_file = "data/web-Stanford.txt"
        gfile = "task7_web_stanford"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        print "Web stanford builded ..."
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles." % r
        drop_if_exists(gfile, self.conn)

    @unittest.skip("")
    def test_roadnet_pa(self):
        """http://snap.stanford.edu/data/roadNet-PA.html"""
        data_file = "data/roadNet-PA.txt"
        gfile = "task7_roadnet_pa"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'))
        print "Roadnet PA builded ..."
        r = count_triangle(gfile, self.conn)
        print "There are %s triangles." % r
        drop_if_exists(gfile, self.conn)