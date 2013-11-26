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