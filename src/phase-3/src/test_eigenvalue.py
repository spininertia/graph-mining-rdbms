import sys

import psycopg2
from eigenvalue.eigen_quodratic import *
from eigenvalue.lanczos import *
from common.basic_operation import *

def test_qeigen_quodratic(conn):
    A = "A1"
    q = "q2"
    r = "r2"
    create_vector_or_matrix(A, conn)
    create_vector_or_matrix(q, conn)
    create_vector_or_matrix(r, conn)
    cur = conn.cursor()
    # cur.execute("insert into %s values (0,0,0.5),(0,1,0.2),(0,2,0.3),(1,0,0.1),(1,1,0.7),(1,2,0.3),(2,0,0.1),(2,1,0.2),(2,2,0.5)" % A)
    cur.execute("insert into %s values (0,0,0.7),(0,1,0.2),(1,0,0.6),(1,1,0.1)" % A)    
    eigen_quodratic(A, q, r, 2, conn)

def test_lanczos(conn):
    b = 'b'
    v = 'v'    
    create_vector_or_matrix(v, conn)
    clear_table("v", conn)
    # random_square_matrix(v, dim, conn);
    cur = conn.cursor()    
    f = open("data/matrix_data.txt")
    data = [line.strip().split(" ") for line in f]
    for i in range(len(data)):
        for j in range(len(data)):
            cur.execute("insert into %s values (%s, %s, %s)" % (v, i, j, data[i][j]))
    dim = len(data)
    create_vector_or_matrix(b, conn)
    for i in range(dim):
        cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
    lanczos(v, b, dim, dim, conn)    

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    test_lanczos(conn)
    # test_qeigen_quodratic(conn)