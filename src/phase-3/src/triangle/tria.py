from common.basic_operation import *
from eigenvalue.eigen_quodratic import *
from eigenvalue.lanczos import *

def count_triangle(tbl_name, conn):
    """ input is a graph """
    tn = "task7_%s_matrix" % tbl_name
    b = 'b'
    cur = conn.cursor()
    create_vector_or_matrix(tn, conn)
    cur.execute("insert into  %s select from_id, to_id, value from %s" % (tn, tbl_name))
    create_vector_or_matrix(b, conn)
    calc_dim_query = "select max(row), max(col) from %s" % (tn)
    cur.execute(calc_dim_query)
    p = cur.fetchone()
    dim = max(p) + 1
    appro = min(dim, 10);
    for i in range(dim):
        cur.execute("insert into %s values (%s, %s, %s)" % (b, i, 0, 1.0 / float(dim)))
    print "dimension is %s" % dim
    lanczos(tn, b, dim, appro, conn)
    cur.execute("select sum(p) from (select power(value,3.0) as p from eigenval where row = col order by value desc limit %s) as d" % appro)
    r = cur.fetchone()
    print "There are %s triangles." % r
    drop_if_exists(tn, conn)
    drop_if_exists(b, conn)