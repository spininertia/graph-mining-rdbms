###########################################
# creation & destop
###########################################
def delete_if_exists(tbl_name, conn):
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
    delete_if_exists(tbl_name, conn)
    cur = conn.cursor()
    cur.execute("create table %s (row int, col int, value float)" % tbl_name)
    conn.commit()

def initilizat_vector():
    pass


###########################################
# read
###########################################
def vector_length(tbl_name, conn):
    """
    normalization length
    """
    cur = conn.cursor()
    cur.execute("select sum(power(value, 2)) from %s" % tbl_name)
    return cur.fetchone()[0]

def matrix_col_length(tbl_name, col, row_low, row_high):
    """
    select sum(val*val) from %s where col = %s and row >= %s and row <= %s
    """
    pass

def matrix_row_length(tbl_name, row, col_low, col_high):
    """
    select sum(val*val) from %s where row = %s and col >= %s and col <= %s
    """
    pass

###########################################
# write
###########################################
def normalize_vector(tbl_name):
    """
    l = vector_length()
    update %s set val = val/%s
    """
    pass

def set_matrix(tbl_name, row, col, v):
    """
    update %s set val = %s where row = %s and col = %s
    """
    pass

def matrix_multiply_matrix_column(tbl1, tbl2, tbl3, col2):
    """
    select V.row, sum(V.val * B.val) from V, B where V.col = B.row and B.col = %s group by V.row
    """

def matrix_multiply_vector(tbl1, tbl2, tbl3):
    pass