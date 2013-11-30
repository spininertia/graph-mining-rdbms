import sys
import time
import unittest
import psycopg2
from common.basic_operation import *
from common.util import *
from pagerank.pagerank import *

class PagerankTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")

    def tearDown(self):
        pass


    def test_dummy_pagerank(self):
        tbl_name = "task2_dummy"
        result_tbl = "task2_dummy_result"
        drop_if_exists(tbl_name, self.conn)
        drop_if_exists(result_tbl, self.conn)
        data = [[0,0,1,0,0,0,0],
                [0,1,1,0,0,0,0],
                [1,0,1,1,0,0,0],
                [0,0,0,1,1,0,0],
                [0,0,0,0,0,0,1],
                [0,0,0,0,0,1,1],
                [0,0,0,1,1,0,1]]
        cur = self.conn.cursor()
        cur.execute("create table %s (from_id int, to_id int)" % tbl_name)
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i][j] == 1:
                    cur.execute("insert into %s values (%s, %s)" % (tbl_name, i, j))
        print "Dummy build"
        calculatepagerank(tbl_name, result_tbl, self.conn)
        normalize_pagerank(result_tbl, self.conn)
        cur = self.conn.cursor()
        cur.execute("select * from %s order by node_id" % result_tbl)
        r = cur.fetchall()
        print r

    @unittest.skip("")
    def test_google_webgraph(self):
        """http://snap.stanford.edu/data/web-Google.html"""
        data_file = "data/web-Google.txt"
        tbl_name = "task2_googleweb"
        result_tbl = "task2_googleweb_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "Google webgraph....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_berkeley_stanford(self):
        """http://snap.stanford.edu/data/web-BerkStan.html"""
        data_file = "data/web-BerkStan.txt"
        tbl_name = "task2_berkstan"
        result_tbl = "task2_berkstan_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "Berkeley stanford....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_web_stanford(self):
        """http://snap.stanford.edu/data/web-Stanford.html"""
        data_file = "data/web-Stanford.txt"
        tbl_name = "task2_webstanford"
        result_tbl = "task2_webstanford_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "Web Stanford....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_amazon_purchase(self):
        """http://snap.stanford.edu/data/com-Amazon.html"""
        # undirected, need reverse
        data_file = "data/com-amazon.ungraph.txt"
        tbl_name = "task2_amazon_product"
        result_tbl = "task2_amazon_product_result"
        load_undirected_graph_into_table(tbl_name, data_file, True, self.conn)
        print "Amazone product....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_slashdot0902(self):
        """http://snap.stanford.edu/data/soc-Slashdot0902.html"""
        data_file = "data/soc-Slashdot0902.txt"
        tbl_name = "task2_slashdot0902"
        result_tbl = "task2_slashdot0902_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "Slashdot0902....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_enron_email(self):
        """http://snap.stanford.edu/data/email-Enron.html"""
        data_file = "data/email-Enron.txt"
        tbl_name = "task2_enronmail"
        result_tbl = "task2_enronmail_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "Enron-mail....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_wiki_vote(self):
        """http://snap.stanford.edu/data/wiki-Vote.html"""
        # directed
        data_file = "data/wiki-Vote.txt"
        tbl_name = "task2_wikivote"
        result_tbl = "task2_wikivote_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "Wiki-cote....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_roadnet_ca(self):
        """http://snap.stanford.edu/data/roadNet-CA.html"""
        # undirected, no reverse
        data_file = "data/roadNet-CA.txt"
        tbl_name = "task2_roadnetca"
        result_tbl = "task2_roadnetca_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "roadNet-CA....."
        calculatepagerank(tbl_name, result_tbl, self.conn)


    @unittest.skip("")
    def test_wiki_talk(self):
        """http://snap.stanford.edu/data/wiki-Talk.html"""
        # directed
        data_file = "data/wiki-Talk.txt"
        tbl_name = "task2_wikitalk"
        result_tbl = "task2_wikitalk_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_roadnet_pa(self):
        """http://snap.stanford.edu/data/roadNet-PA.html"""
        # undirected, no reverse
        data_file = "data/roadNet-PA.txt"
        tbl_name = "task2_roadnetpa"
        result_tbl = "task2_roadnetpa_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "roadNet-PA....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_roadnet_tx(self):
        """http://snap.stanford.edu/data/roadNet-TX.html"""
        # undirected, no reverse
        data_file = "data/roadNet-TX.txt"
        tbl_name = "task2_roadnettx"
        result_tbl = "task2_roadnettx_result"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "roadNet-TX....."
        calculatepagerank(tbl_name, result_tbl, self.conn)

    @unittest.skip("")
    def test_youtube(self):
        """http://snap.stanford.edu/data/com-Youtube.html"""
        # undirected, need reverse
        data_file = "data/com-youtube.ungraph.txt"
        tbl_name = "task2_youtube"
        result_tbl = "task2_youtube_result"
        load_undirected_graph_into_table(tbl_name, data_file, True, self.conn)
        calculatepagerank(tbl_name, result_tbl, self.conn)