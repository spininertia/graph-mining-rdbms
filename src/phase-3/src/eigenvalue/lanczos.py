from common.basic_operation import *
from eigen_quodratic import *

def lanczos(A, b, n, m, conn):
    """
    A: n X n matrix
    b: initial vector
    m: number of steps
    """
    beta = "beta"
    v = ["v%s" % i for i in range(m+2)] # TODO: why this fixed? 
    v_tmp = "v_tmp"
    alpha = "alpha"

    create_vector_or_matrix(beta, conn) # just empty
    for v_table in v:
        create_vector_or_matrix(v_table, conn) # just empty
    create_vector_or_matrix(v_tmp, conn) # just empty
    create_vector_or_matrix(alpha, conn) # just empty
    initilizat_vector(beta, m+1, conn) # beta_0 = 0
    initilizat_vector(v[0], n, conn) # v_0 = {0}
    initilizat_vector(alpha, m+1, conn)
    create_vector_or_matrix(v[1], conn) # empty v1
    assign_to(b, v[1], conn) # v_1 = b
    normalize_vector(v[1], conn) # v_1 = b/|b|
    index_counter = 0
    for i in range(1, m):
        print "Iteration: %s" % i
        matrix_multiply_vector_overwrite(A, v[i], v_tmp, conn) # v = A * v_i
        alpha_i = vector_dot_product(v[i], v_tmp, conn) # alpha_i = v_i * v
        set_matrix(alpha, i, 0, alpha_i, conn)

        cur = conn.cursor()
        cur.execute("select value from %s where row = %s" % (beta, i-1))
        beta1 = cur.fetchone()[0]
        cur.execute("select value from %s where row = %s" % (alpha, i))
        alpha1 = cur.fetchone()[0]
        cur.execute("create index vindex%s ON %s (row)" % (index_counter, v[i-1]))
        index_counter += 1
        cur.execute("create index vindex%s ON %s (row)" % (index_counter, v[i]))
        index_counter += 1
        print "index builded...."
        cur.execute("""
            update %s set value = 
            value - %s * (select value from %s where row = %s.row) 
                  - %s * (select value from %s where row = %s.row)""" % \
                  (v_tmp, beta1, v[i-1], v_tmp, alpha1, v[i], v_tmp))
        print "vector update done"
        vl = vector_length(v_tmp, conn) # |v|
        set_matrix(beta, i, 0, vl, conn) # beta_i = |v|
        if (vl == 0):
            break
        create_vector_or_matrix(v[i+1], conn) # just empty
        assign_to(v_tmp, v[i+1], conn) # v_i+1 = v
        cur = conn.cursor()
        cur.execute("update %s set value = value / (select value from %s where row = %s)" % (v[i+1], beta, i))
    cur = conn.cursor()
    V_mat = "v_matrix"
    create_vector_or_matrix(V_mat, conn)
    print "The width is %s" % len(v)
    for i in range(m):
        vvv = v[i]
        print "appending %s" % vvv
        cur.execute("insert into %s select row, %s, value from %s" % (V_mat, i, vvv))
        drop_if_exists(vvv, conn)    
    ritz_vector(alpha, beta, m, V_mat, conn)
    drop_if_exists('alpha', conn)
    drop_if_exists('beta', conn)
    drop_if_exists('b', conn)
    drop_if_exists('t', conn)
    drop_if_exists('v', conn)
    drop_if_exists('v_tmp', conn)    

def ritz_vector(alpha, beta, m, V, conn):
    """
    solve eigenvector for a smaller martix
    """
    t = "t"
    print "Building triagonal matrix"
    build_tridiagonal_matrix(alpha, beta, m, t, conn)
    print "QR decomposition"
    eigen_quodratic(t, 'eigenvec_tmp', 'eigenval', m, conn)
    print "Calculating eigen vectors....."
    matrix_multiply_matrix_overwrite(V, 'eigenvec_tmp', 'eigenvec', conn)
    drop_if_exists("eigenvec_tmp", conn)
    print "Eigenvector calculated, they are stored in %s and %s" % ('eigenval', 'eigenvec')

def build_tridiagonal_matrix(alpha, beta, m, t, conn):
    create_vector_or_matrix(t, conn) # just empty
    cur = conn.cursor()
    for i in range(1, m+1):
        for j in range(1, m+1):
            if j == i:
                # print cur.mogrify("insert into %s select %s, %s, value from %s where row = %s" % (t, i-1, i-1, alpha, i)) # T[i, i] <- alpha_i        
                cur.execute("insert into %s select %s, %s, value from %s where row = %s" % (t, i-1, i-1, alpha, i)) # T[i, i] <- alpha_i        
            elif j == i + 1:
                cur.execute("insert into %s select %s, %s, value from %s where row = %s" % (t, i-1, j-1, beta, i))        
            elif i - 1 >= 1 and j == i - 1:
                cur.execute("insert into %s select %s, %s, value from %s where row = %s" % (t, i-1, i-2, beta, i-1))        
            else:
                # print cur.mogrify("insert into %s values (%s, %s, 0.0)" % (t, i-1, j-1))
                cur.execute("insert into %s values (%s, %s, 0.0)" % (t, i-1, j-1))
    conn.commit()









