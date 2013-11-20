import psycopg2
import sys

def drop_if_exists(tbl_name, conn):
    """
    delete a table if exists
    """
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % tbl_name)
    conn.commit()


def mst(conn, edge_table, dataset):
	"""
	Prim's algorithm
	"""
	cur = conn.cursor()
	target_table = "mst_" + dataset
	node_table = "node_mst"
	tmp_table = "tmp_table"
	drop_if_exists(target_table, conn)
	drop_if_exists(node_table, conn)
	drop_if_exists(tmp_table, conn)
	cur.execute("create table %s(src_id int, dst_id int, weight float)" % target_table)
	cur.execute("create table %s(nid int)" % node_table)
	cur.execute("create table %s(src_id int, dst_id int, weight float)" % tmp_table);
	conn.commit()
	cur.execute('select count(distinct src_id)from %s' % edge_table)
	num_nodes = cur.fetchone()[0]
	# randomly insert an initial node 
	cur.execute('insert into %s select src_id from %s limit 1' % (node_table, edge_table))
	conn.commit()
	for i in range(num_nodes - 1):
		cur.execute("""insert into %s select src_id, dst_id, weight from %s as A, %s as B 
			where A.src_id = B.nid AND A.dst_id not in (select nid from %s) order by weight limit 1""" % (tmp_table, edge_table, node_table, node_table))
		cur.execute('insert into %s select dst_id from %s' % (node_table, tmp_table))
		cur.execute('insert into %s select * from %s' % (target_table, tmp_table))
		cur.execute('delete from %s' % tmp_table)
		conn.commit()

if __name__ == "__main__":
	conn = psycopg2.connect(database="mydb", host="127.0.0.1")
	mst(conn, sys.argv[1], sys.argv[2])

