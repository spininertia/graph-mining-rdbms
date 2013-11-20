import sys
import time
import psycopg2
from common.basic_operation import *
from common.util import *
from pagerank.pagerank import *

def time_it(fn):
    def wrapped(*args):
        start = time.time()
        fn(*args)
        used = time.time() - start
        print "Used %s seconds. " % used
    return wrapped

@time_it
def test_route_view(conn):
    tbl_name = 'edge_un_route'
    data_file = 'data/as20000102.txt'
    load_undirected_graph_into_table(tbl_name, data_file, True, conn)
    print "[pagerank]testing route view"
    print "data loaded"
    calculatepagerank(tbl_name, "pagerank_route", conn)
    print "calculation done"

@time_it
def test_google_plus(conn):
    tbl_name = 'edge_googleplu'
    data_file = 'data/gplus_undirected.txt'
    load_undirected_graph_into_table(tbl_name, data_file, False, conn)
    print "[pagerank]testing google plus"
    print "data loaded"
    calculatepagerank(tbl_name, "pagerank_gplus", conn)
    print "calculation done"

@time_it
def test_advogo(conn):
    tbl_name = 'edge_advogato'
    data_file = 'data/advogato_undirected.txt'
    load_undirected_graph_into_table(tbl_name, data_file, False, conn)
    print "[pagerank]testing advogato"
    print "data loaded"
    calculatepagerank(tbl_name, "pagerank_advotago", conn)
    print "calculation done"    

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_route_view(conn)
    # test_google_plus(conn)
    # test_advogo(conn)
