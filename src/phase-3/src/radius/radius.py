def assign_fm(conn, tbl_name, edge_table):
	cur = conn.cursor()
	cur.execute("delete from %s" % tbl_name)
	cur.execute("insert into %s select src_id, fm_assign(32) from %s group by src_id" % (tbl_name, edge_table))
	conn.commit()

	cur.close()

def update_bitstring(conn, edge_table, vertex_table, tmp_table):
	cur = conn.cursor()
	cur.execute("delete from %s" % tmp_table)
	cur.execute("insert into %s select src_id, agg_bit_or(fm) from %s, %s where dst_id = id group by src_id" %(tmp_table, edge_table, vertex_table))
	conn.commit()
	cur.close()


def is_stablized(conn, vertex_table, tmp_table):
	cur = conn.cursor()
	diff = cur.execute("select count(*) from %s, %s where %s.id = %s.id and %s.fm <> %s.fm" % (vertex_table, tmp_table, vertex_table, tmp_table, vertex_table, tmp_table))
	diff = cur.fetchone()[0]
	if diff == 0:
		return True
	else:
		return False

def record_hops(conn, hop_table, vertex_table, hop):
	cur = conn.cursor()
	cur.execute("insert into %s select id, %d, fm_size(fm) from %s" %(hop_table, hop, vertex_table))
	conn.commit()
	cur.close()

def drop_if_exists(conn, table_name):
	cur = conn.cursor()
	cur.execute("drop table if exists %s" % table_name)
	conn.commit()
	cur.close()

def radius(conn, edge_table, dataset):
	"""
	edge_table: edge table
	"""
	vertex_table = "vertex"
	tmp_table = "tmp_v"
	hop_table = "hops"
	tmp_edge = "tmp_edge"
	radius_table = dataset + "radius"
	cur = conn.cursor()
	drop_if_exists(conn, tmp_table)
	drop_if_exists(conn, vertex_table)
	drop_if_exists(conn, hop_table)
	drop_if_exists(conn, tmp_edge)
	drop_if_exists(conn, radius_table)
	cur.execute("select * into %s from %s" % (tmp_edge, edge_table))
	cur.execute("insert into %s select src_id, src_id, 1.0 from %s group by src_id" % (tmp_edge, edge_table))
	edge_table = tmp_edge
	cur.execute("create table %s(id int, fm bit(32)[])" % vertex_table)
	cur.execute("create table %s(id int, fm bit(32)[])" % tmp_table)
	cur.execute("create table %s(id int, hop int, size float)" % hop_table)
	cur.execute("create table %s(id int, radius int)" % radius_table)
	conn.commit()

	assign_fm(conn, vertex_table, edge_table)
	record_hops(conn, hop_table, vertex_table, 0)

	max_iteration = 256
	for i in range(max_iteration):
		print "interation %d" % i
		if (i != 0):
			cur.execute("delete from %s" % vertex_table)
			cur.execute("insert into %s select * from %s" % (vertex_table, tmp_table))
			conn.commit()
		update_bitstring(conn, edge_table, vertex_table, tmp_table)
		if (is_stablized(conn, vertex_table, tmp_table)):
			break
		record_hops(conn, hop_table, tmp_table, i + 1)
	cur.execute("""
		insert into %(rad)s	
		select %(hop)s.id as id, min(%(hop)s.hop) as radius from %(hop)s, (select id, max(size) as max_size from %(hop)s group by id) as foo
		where %(hop)s.id = foo.id and %(hop)s.size = foo.max_size
		group by %(hop)s.id;		
		""" % {'rad':radius_table, 'hop':hop_table})
	conn.commit()
	cur.close()
	conn.close()

