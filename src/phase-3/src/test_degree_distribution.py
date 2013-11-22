import sys
import time
import psycopg2
import unittest

from common.util import *
from ddis.ddis import *

class DegreeDistributionTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")

    def tearDown(self):
        pass

    @unittest.skip("skip roadnet ca")
    def test_roadnet_ca(self):
        """http://snap.stanford.edu/data/roadNet-CA.html"""
        # undirected, no reverse
        data_file = "data/roadNet-CA.txt"
        tbl_name = "task1_roadnetca"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "roadNet-CA....."
        undirect_dis(tbl_name, 'task1_roadnetca_result', self.conn)

    def test_wiki_talk(self):
        """http://snap.stanford.edu/data/wiki-Talk.html"""
        # directed
        data_file = "data/wiki-Talk.txt"
        tbl_name = "task1_wikitalk"
        result_tbl = "task1_wikitalk_result_"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        indis(tbl_name, result_tbl+"in", self.conn)
        outdis(tbl_name, result_tbl+"out", self.conn)

    @unittest.skip("")
    def test_roadnet_pa(self):
        """http://snap.stanford.edu/data/roadNet-PA.html"""
        # undirected, no reverse
        data_file = "data/roadNet-PA.txt"
        tbl_name = "task1_roadnetpa"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "roadNet-PA....."
        undirect_dis(tbl_name, 'task1_roadnetpa_result', self.conn)

    @unittest.skip("")
    def test_roadnet_tx(self):
        """http://snap.stanford.edu/data/roadNet-TX.html"""
        # undirected, no reverse
        data_file = "data/roadNet-TX.txt"
        tbl_name = "task1_roadnettx"
        load_undirected_graph_into_table(tbl_name, data_file, False, self.conn)
        print "roadNet-TX....."
        undirect_dis(tbl_name, 'task1_roadnettx_result', self.conn)

    @unittest.skip("")
    def test_youtube(self):
        """http://snap.stanford.edu/data/com-Youtube.html"""
        # undirected, need reverse
        data_file = "data/com-youtube.ungraph.txt"
        tbl_name = "task1_youtube"
        result_tbl = "task1_youtube_result"
        load_undirected_graph_into_table(tbl_name, data_file, True, self.conn)
        undirect_dis(tbl_name, result_tbl, self.conn)

# @time_it    
# def test_route_view(conn):
#     tbl_name = 'task1_edge_un_route'
#     data_file = 'data/as20000102.txt'
#     load_undirected_graph_into_table(tbl_name, data_file, True, conn)
#     print "[degree distribution]testing route view"
#     print "data loaded"
#     undirect_dis(tbl_name, 'task1_un_route', conn)
#     print "calculation done"

# @time_it
# def test_gplus(conn):
#     tbl_name = 'task1_edge_gplus'
#     data_file = 'data/gplus_directed.txt'
#     load_undirected_graph_into_table(tbl_name, data_file, False, conn)
#     print "[degree distribution]testing google plus"
#     print "data loaded"
#     indis(tbl_name, "task1_in_gplus", conn)
#     outdis(tbl_name, "task1_out_gplus", conn)
#     print "calculation done"

# @time_it
# def test_advogato(conn):
#     tbl_name = 'task1_edge_advogato'
#     data_file = 'data/advogato_undirected.txt'
#     load_undirected_graph_into_table(tbl_name, data_file, False, conn)
#     print "[degree distribution]testing advogato"
#     print "data loaded"
#     indis(tbl_name, "task1_in_advogato", conn)
#     outdis(tbl_name, "task1_out_advogato", conn)
#     print "calculation done"        
