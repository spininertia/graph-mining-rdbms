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
    initialize a vector to zero
    """
    clear_table(tbl_name, conn)
    cur = conn.cursor()
    # this is slow, I know
    for i in range(dim):
        cur.execute("insert into %s values (%s, 0, 0.0)" % (tbl_name, i))
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
def clear_table(tbl_name, conn):
    cur = conn.cursor()
    cur.execute("delete from %s" % tbl_name)
    conn.commit()

def matrix_multiply_matrix_overwrite(a, b, result, conn):
    clear_table(result, conn);
    cur = conn.cursor()
    cur.execute("insert into %s select A.row, B.col, sum(A.value * B.value) from %s A, %s B where A.col = B.row group by A.row, B.col" % (result, a, b))
    conn.commit()

def matrix_multiply_vector_overwrite(a, b, c, conn):
    """
    a X b = c
    """
    clear_table(c, conn)
    cur = conn.cursor()
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

def set_matrix(tbl_name, row, col, v):
    """
    update a cell in matrix
    """
    cur = conn.cursor()
    cur.execute("update %s set value = %s where row = %s and col = %s" % (tbl_name, v, row, col))
    conn.commit()