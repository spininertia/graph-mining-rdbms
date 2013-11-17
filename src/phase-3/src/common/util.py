#######################
# Load file
#######################e
def load_undirected_graph_into_table(tbl_name, filename, doreverse, conn):
    """ load an undirected unweighted file into a (from_id, to_id) pair"""
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % tbl_name)
    cur.execute("create table %s(from_id int, to_id int)" % tbl_name)
    conn.commit()
    with open(filename) as f:
        cur.copy_from(f, tbl_name, columns=('from_id', 'to_id'))
    if doreverse:
        cur.execute("insert into %s select to_id, from_id from %s" % (tbl_name, tbl_name))
    conn.commit()        


def convert_matrix_from_graph():
    pass