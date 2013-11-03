from common.basic_operation import *

## QR factorization of matrix
def qr_decompose(v, q, r, dim, conn):
    """
    v: original matrix
    q: left matrix
    r: right matrix
    dim: dimension of v

    1. assume q,r are empty
    2. v is square matrix
    """
    # copy v to q
    cur = conn.cursor()
    cur.execute("delete from %s" % q)
    cur.execute("delete from %s" % r)
    cur.execute("insert into %s select * from %s" % (q, v))
    conn.commit()
    for i in range(0, dim):
        cur.execute("insert into %s select %s, %s, sqrt(sum(power(value, 2))) from %s where col = %s" % (r, i, i, q, i))
        conn.commit()
        normalize_column(q, i, conn)

        for j in range(i+1, dim):
            cur.execute("(select sum(Q1.value * Q2.value) from %s Q1, %s Q2 where Q1.row = Q2.row and Q1.col = %s and Q2.col = %s)" % (q, q, i, j))
            r_i_j = cur.fetchone()[0]
            cur.execute("insert into %s values (%s, %s, %s)" % (r, i, j, r_i_j))
            cur.execute("update %s Q1 set value = value - %s * (select value from %s Q2 where Q2.row = Q1.row and Q2.col = %s) where col = %s" % (q, r_i_j, q, i, j))
            conn.commit()

