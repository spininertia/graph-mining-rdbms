from common.basic_operation import *
from eigenvalue.eigen_quodratic import *
from eigenvalue.lanczos import *

def count_triangle(tbl_name, conn):
    """ input is a matrix """
    b = 'b'
    lim = 15
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
    cur.execute("select sum(p)/6 from (select power(value,3.0) as p from eigenval where row = col order by value desc limit %s) as d" % appro)
    r = cur.fetchone()
    drop_if_exists(tn, conn)
    drop_if_exists(b, conn)
    return r