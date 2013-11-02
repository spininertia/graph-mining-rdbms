###########################################
# creation & destop
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
    cur.execute("select sqrt(sum(power(value, 2))) from %s" % tbl_name)
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
def clear_table(tbl_name, conn):
    cur = conn.cursor()
    cur.execute("delete from %s" % tbl_name)
    conn.commit()

def matrix_multiply_matrix_overwrite(a, b, result, conn):
    clear_table(result, conn);
    cur = conn.cursor()
    cur.execute("insert into %s select A.row, B.col, sum(A.value * B.value) from %s A, %s B where A.col = B.row group by A.row, B.col" % (result, a, b))
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