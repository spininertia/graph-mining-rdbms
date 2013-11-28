from common.basic_operation import *
from eigenvalue.eigen_quodratic import *
from eigenvalue.lanczos import *

def count_triangle(tbl_name, conn):
    """ input is a matrix """
    tol = 0.1
    b = 'b'
    lim = 30
    cur = conn.cursor()
    tn = tbl_name
    print "create matrix..."
    create_vector_or_matrix(b, conn)
    print "Counting dimension..."
    calc_dim_query = "select max(row), max(col) from %s" % (tn)
    cur.execute(calc_dim_query)
    p = cur.fetchone()
    dim = max(p) + 1
    print "dimension is %s" % dim    
    appro = min(dim, lim);
    for i in range(dim):
        cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
    print "init b..."
    lanczos(tn, b, dim, appro, conn)
    cur.execute("select power(value,3.0) from eigenval where row = col order by value desc limit %s" % appro)
    r = cur.fetchall()
    print r
    s = 0.0001
    for i in range(len(r)):
        if r[i][0] < 0 or abs(r[i][0]) / s < tol:
            break
        s += r[i][0]
    drop_if_exists(tn, conn)
    drop_if_exists(b, conn)
    # drop_if_exists("eigenval", conn)
    # drop_if_exists("eigenvec", conn)
    return s / 6.0

def count_local_triangle(tbl_name, conn):
    pass