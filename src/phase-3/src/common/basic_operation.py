###########################################
# creation & destroy
###########################################
def drop_if_exists(tbl_name, conn):
    """
    delete a table if exists
    """
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % tbl_name)
    conn.commit()

def create_vector_or_matrix(tbl_name, conn):
    """
    create an *empty* vector or matrix
    """
    drop_if_exists(tbl_name, conn)
    cur = conn.cursor()
    cur.execute("create table %s (row int, col int, value float)" % tbl_name)
    conn.commit()

def initilizat_vector(tbl_name, dim, conn):
    """
    initilize a vector
    """
    import random
    clear_table(tbl_name, conn)
    cur = conn.cursor()
    # this is slow, I know
    for i in range(dim):
        cur.execute("insert into %s values (%s, 0, %s)" % (tbl_name, i, 0.0))
    conn.commit()

def initilizat_square_matrix(tbl_name, dim, conn):
    """
    initilize a matrix
    """
    import random
    clear_table(tbl_name, conn)
    cur = conn.cursor()
    # this is slow, I know
    for i in range(dim):
        for j in range(dim):
            cur.execute("insert into %s values (%s, %s, %s)" % (tbl_name, i, j, 0.0))
    conn.commit()    

def random_vector(tbl_name, dim, conn):
    """
    randomly initilize a vector
    """
    import random
    clear_table(tbl_name, conn)
    cur = conn.cursor()
    # this is slow, I know
    for i in range(dim):
        cur.execute("insert into %s values (%s, 0, %s)" % (tbl_name, i, random.uniform(0, 1)))
    conn.commit()

def random_square_matrix(tbl_name, dim, conn):
    """
    randomly initilize a matrix
    """
    import random
    clear_table(tbl_name, conn)
    cur = conn.cursor()
    # this is slow, I know
    for i in range(dim):
        for j in range(dim):
            cur.execute("insert into %s values (%s, %s, %s)" % (tbl_name, i, j, random.uniform(0, 1)))
    conn.commit()    

def assign_to(from_tbl, to_tbl, conn):
    """
    assign a vector/matrix to another variable(table)
    """
    clear_table(to_tbl, conn)
    cur = conn.cursor()
    cur.execute("insert into %s select * from %s" % (to_tbl, from_tbl))
    conn.commit()


###########################################
# read
###########################################
def vector_length(tbl_name, conn):
    """
    normalization length
    """
    cur = conn.cursor()
    cur.execute("select sqrt(sum(power(value, 2))) from %s" % tbl_name)
    return cur.fetchone()[0]

def vector_dot_product(a, b, conn):
    """
    a .X b
    """
    cur = conn.cursor()
    cur.execute("select sum(A.value * B.value) from %s A, %s B where A.row = B.row" % (a, b))
    return cur.fetchone()[0]

###########################################
# write
###########################################
def reverse_edge(tbl, conn):
    cur = conn.cursor()
    cur.execute("insert into %s select to_id, from_id, value from %s" % (tbl, tbl))
    conn.commit()

def reverse_matrix(tbl, conn):
    cur = conn.cursor()
    cur.execute("insert into %s select col, row, value from %s" % (tbl, tbl))
    conn.commit()

def clear_table(tbl_name, conn):
    cur = conn.cursor()
    cur.execute("delete from %s" % tbl_name)
    conn.commit()

def matrix_multiply_matrix_overwrite(a, b, result, conn):
    create_vector_or_matrix(result, conn)
    cur = conn.cursor()
    cur.execute("insert into %s select A.row, B.col, sum(A.value * B.value) from %s A, %s B where A.col = B.row group by A.row, B.col" % (result, a, b))
    conn.commit()

def matrix_multiply_vector_overwrite(a, b, c, conn):
    """
    a X b = c
    """
    clear_table(c, conn)
    cur = conn.cursor()
    cur.mogrify("insert into %s select A.row, 0, sum(A.value * B.value) from %s A, %s B where A.col = B.row group by A.row" % (c, a, b))    
    cur.execute("insert into %s select A.row, 0, sum(A.value * B.value) from %s A, %s B where A.col = B.row group by A.row" % (c, a, b))
    conn.commit()

def matrix_multiply_matrix_ignore(a, b, result, conn):
    """
    seem like not easy to do with PostSQL
    """
    pass


def normalize_vector(tbl_name, conn):
    """
    normalized vector
    """
    l = vector_length(tbl_name, conn)
    cur = conn.cursor()
    cur.execute("update %s set value = value / %s" % (tbl_name, l))
    conn.commit()

def normalize_column(tbl_name, col, conn):
    """
    normalize a column of a matrix
    """
    cur = conn.cursor()
    cur.execute("select sqrt(sum(power(value, 2))) from %s where col = %s" % (tbl_name, col))
    l = cur.fetchone()[0]
    if l > 0:
        cur.execute("update %s Q1 set value = value / %s where col = %s" % (tbl_name, l, col))
    conn.commit()

def devide_column(tbl_name, col, d, conn):
    """
    devide a column of a matrix by a constance
    """
    cur = conn.cursor()
    cur.execute("update %s Q1 set value = value / %s where col = %s" % (tbl_name, d, ol))
    conn.commit()    

def set_matrix(tbl_name, row, col, v, conn):
    """
    update a cell in matrix
    """
    cur = conn.cursor()
    cur.execute("update %s set value = %s where row = %s and col = %s" % (tbl_name, v, row, col))
    conn.commit()