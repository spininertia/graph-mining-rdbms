import sys
import time
import unittest
import psycopg2
from common.basic_operation import *
from common.util import *
from eigenvalue.lanczos import *

class EigenvalueTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")

    def tearDown(self):
        pass

    @unittest.skip("")
    def test_ucidata(self):
        data_file = "data/ucidata-zachary.txt"
        gfile = "task5_ucidata"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'), sep=" ")
        cur.execute("update %s set col=col-1, row=row-1" % gfile)
        self.conn.commit()
        print "Ucidata builded ..."
        reverse_matrix(gfile, self.conn)
        b = 'b'
        create_vector_or_matrix(b, self.conn)
        cur.execute("select max(col) from %s" % gfile)
        dim = cur.fetchone()[0] + 1
        print "Dimension is %s" % dim
        for i in range(dim):
            cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
        lanczos(gfile, b, dim, 20, self.conn)    
        drop_if_exists(b, self.conn)

    @unittest.skip("")
    def test_dblp_cite(self):
        """http://konect.uni-koblenz.de/networks/dblp-cite"""
        data_file = "data/dblp-cite.txt"
        gfile = "task5_dblpcite"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'), sep=" ")
        cur.execute("update %s set col=col-1, row=row-1" % gfile)
        self.conn.commit()
        print "DBLP builded ..."
        reverse_matrix(gfile, self.conn)
        b = 'b'
        create_vector_or_matrix(b, self.conn)
        cur.execute("select max(col) from %s" % gfile)
        dim = cur.fetchone()[0] + 1
        print "Dimension is %s" % dim
        for i in range(dim):
            cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
        lanczos(gfile, b, dim, 20, self.conn)    
        drop_if_exists(b, self.conn)

    @unittest.skip("")
    def test_youtube(self):
        """http://snap.stanford.edu/data/com-Youtube.html"""
        data_file = "data/com-youtube.ungraph.txt"
        gfile = "task5_youtube"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.copy_from(open(data_file), gfile, columns=('row', 'col'), sep="\t")
        cur.execute("update %s set col=col-1, row=row-1" % gfile)
        self.conn.commit()
        print "Youtube builded ..."
        reverse_matrix(gfile, self.conn)
        b = 'b'
        create_vector_or_matrix(b, self.conn)
        cur.execute("select max(col) from %s" % gfile)
        dim = cur.fetchone()[0] + 1
        print "Dimension is %s" % dim
        for i in range(dim):
            cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
        lanczos(gfile, b, dim, 20, self.conn)    
        drop_if_exists(b, self.conn)

    @unittest.skip("")
    def test_uci_gamma(self):
        """http://konect.uni-koblenz.de/networks/ucidata-gama"""
        data_file = "data/ucidata-gama.txt"
        gfile = "task5_ucigama"
        cur = self.conn.cursor()
        drop_if_exists(gfile, self.conn)
        cur.execute("create table %s(row int, col int, value real DEFAULT 1)" % (gfile))
        cur.execute("create table tmppppp(row int, col int, value real DEFAULT 1)")
        cur.copy_from(open(data_file), "tmppppp", columns=('row', 'col', 'value'), sep="\t")
        cur.execute("insert into %s select row, col from tmppppp" % gfile)
        drop_if_exists("tmppppp", self.conn)
        cur.execute("update %s set col=col-1, row=row-1" % gfile)
        self.conn.commit()
        print "Uci gama builded ..."
        reverse_matrix(gfile, self.conn)
        b = 'b'
        create_vector_or_matrix(b, self.conn)
        cur.execute("select max(col) from %s" % gfile)
        dim = cur.fetchone()[0] + 1
        print "Dimension is %s" % dim
        for i in range(dim):
            cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
        lanczos(gfile, b, dim, 20, self.conn)    
        drop_if_exists(b, self.conn)