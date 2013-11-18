import sys
import time
import psycopg2

from common.util import *
from ddis.ddis import *

def time_it(fn):
    def wrapped(*args):
        start = time.time()
        fn(*args)
        used = time.time() - start
        print "Used %s seconds. " % used
    return wrapped

@time_it    
def test_route_view(conn):
    tbl_name = 'task1_edge_un_route'
    data_file = 'data/as20000102.txt'
    load_undirected_graph_into_table(tbl_name, data_file, True, conn)
    print "[degree distribution]testing route view"
    print "data loaded"
    undirect_dis(tbl_name, 'task1_un_route', conn)
    print "calculation done"

@time_it
def test_gplus(conn):
    tbl_name = 'task1_edge_gplus'
    data_file = 'data/gplus_directed.txt'
    load_undirected_graph_into_table(tbl_name, data_file, False, conn)
    print "[degree distribution]testing google plus"
    print "data loaded"
    indis(tbl_name, "task1_in_gplus", conn)
    outdis(tbl_name, "task1_out_gplus", conn)
    print "calculation done"

@time_it
def test_advogato(conn):
    tbl_name = 'task1_edge_advogato'
    data_file = 'data/advogato_undirected.txt'
    load_undirected_graph_into_table(tbl_name, data_file, False, conn)
    print "[degree distribution]testing advogato"
    print "data loaded"
    indis(tbl_name, "task1_in_advogato", conn)
    outdis(tbl_name, "task1_out_advogato", conn)
    print "calculation done"        

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_route_view(conn)
    # test_gplus(conn)
    # test_advogato(conn)