from common.basic_operation import *
from eigen_quodratic import *

def lanczos(A, b, n, m, conn):
    """
    A: n X n matrix
    b: initial vector
    m: number of steps
    """
    beta = "beta"
    v = ["v%s" % i for i in range(m+1)]
    v_tmp = "v_tmp"
    alpha = "alpha"

    create_vector_or_matrix(beta, conn) # just empty
    create_vector_or_matrix(v,    conn) # just empty
    create_vector_or_matrix(v_tmp, conn) # just empty
    create_vector_or_matrix(alpha, conn) # just empty
    initilizat_vector(beta, m, conn) # beta_0 = 0
    initilizat_vector(v[0], n, conn) # v_0 = {0}
    initilizat_vector(alpha, m+1, conn)
    create_vector_or_matrix(v[1], conn) # empty v1
    assign_to(b, v[1], conn) # v_1 = b
    normalize_vector(v[1], conn) # v_1 = b/|b|
    for i in range(1, m+1):
        matrix_multiply_vector_overwrite(a, v[i], v_tmp, conn) # v = A * v_i
        alpha_i = vector_dot_product(v[i], v_tmp) # alpha_i = v_i * v
        set_matrix(alpha, i, alpha_i, conn)

        cur = conn.cursor()
        cur.execute("update %s set value = value - (select value from %s where row = %s) * (select value from %s where row = %s) - (select value from %s where row = %s) * (select value from %s where row = %s)" % (v_tmp, beta, i-1, v[i-1], i, alpha, i, v[i], i))
        conn.commit()

        vl = vector_length(v_tmp, conn) # |v|
        set_matrix(beta, i, 0, vl) # beta_i = |v|
        if (vl == 0):
            break
        create_vector_or_matrix(v[i+1], conn) # just empty
        assign_to(v_tmp, v[i+1], conn) # v_i+1 = v
        cur = conn.cursor()
        cur.execute("update %s set value = value / (select value from %s where row = %s)" % (v[i+1], beta, i))
    # copy v into a matrix, they are still separate vector now
    # seems like V is useless, so I would not bother transform it.
    ritz_vector(alpha, beta, m, conn)

def ritz_vector(alpha, beta, m, conn):
    """
    solve eigenvector for a smaller martix
    """
    t = build_tridiagonal_matrix(alpha, beta, m, conn)
    eigen_quodratic(t, 'eigenval', 'eigenvec', m, conn)
    print "Eigenvector calculated, they are stored in %s and %s" % ('eigenval', 'eigenvec')



