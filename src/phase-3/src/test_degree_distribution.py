import sys
import psycopg2

from common.util import *
from ddis.ddis import *

def test_route_view(conn):
    tbl_name = 'edge_route'
    data_file = 'data/as20000102.txt'
    load_undirected_graph_into_table(tbl_name, data_file, True, conn)
    print "[degree distribution]testing route view"
    print "data loaded"
    undirect_dis(tbl_name, 'degree_distribution_route', conn)
    print "calculation done"

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_route_view(conn)