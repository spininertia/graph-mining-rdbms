import sys

def time_it(fn):
	def wrapped(*args):
		import time
		start = time.time()
		fn(*args)
		used = time.time() - start
		print "used %s" % used
	return wrapped

@time_it
def assign_fm(conn, tbl_name, edge_table):
	cur = conn.cursor()
	cur.execute("delete from %s" % tbl_name)
	cur.execute("insert into %s select src_id, fm_assign(4) from %s group by src_id" % (tbl_name, edge_table))
	conn.commit()

	cur.close()

@time_it
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



@time_it
def summarize(conn, radius_table, dataset):
	cur = conn.cursor()
	drop_if_exists(conn, "tmp")
	cur.execute("select radius, count(*) into tmp from %s group by radius order by radius" % radius_table)
	f = open('radius_' + dataset + ".csv", 'w')
	cur.copy_to(sys.stdout, "tmp", sep = ',')
	cur.copy_to(f, "tmp", sep = ',')

def radius(conn, edge_table, dataset):
	"""
	edge_table: edge table
	"""
	vertex_table = "vertex"
	tmp_table = "tmp_v"
	hop_table = "hops"
	tmp_edge = "tmp_edge"
	radius_table = "radius_" + dataset
	cur = conn.cursor()
	drop_if_exists(conn, tmp_table)
	drop_if_exists(conn, vertex_table)
	drop_if_exists(conn, tmp_edge)
	drop_if_exists(conn, radius_table)
	cur.execute("create table %s(src_id int, dst_id int)" % tmp_edge)
	cur.execute("insert into %s select src_id, dst_id from %s" % (tmp_edge, edge_table))
	cur.execute("insert into %s select src_id, src_id from %s group by src_id" % (tmp_edge, edge_table))
	#cur.execute("insert into %s select dst_id, dst_id from %s where dst_id not in (select src_id from %s) group by dst_id" % (tmp_edge, edge_table, edge_table))
	#cur.execute("drop index if exists radius_index ")
	#cur.execute("create index radius_index on %s (src_id) " % edge_table)

	cur.execute("create table %s(id int, fm bit(32)[])" % vertex_table)
	cur.execute("create table %s(id int, fm bit(32)[])" % tmp_table)

	cur.execute("create table %s(id int, radius int)" % radius_table)

	cur.execute("drop index if exists radius_index")
	cur.execute("drop index if exists edge_index")
	cur.execute("create index edge_index on %s (src_id, dst_id)" % tmp_edge )
	cur.execute("create index radius_index on %s(id)" % vertex_table)
	conn.commit()

	assign_fm(conn, vertex_table, tmp_edge)
 	
	max_iteration = 256
	for i in range(max_iteration):
		print "iteration %d" % i
		if (i != 0):
			cur.execute("delete from %s" % vertex_table)
			cur.execute("insert into %s select * from %s" % (vertex_table, tmp_table))
			conn.commit()
		update_bitstring(conn, tmp_edge, vertex_table, tmp_table)
		if (is_stablized(conn, vertex_table, tmp_table)):
			break
		cur.execute("insert into %s select A.id, %d from %s as A, %s as B where A.id = B.id and A.fm = B.fm and A.id not in (select id from %s)" % (radius_table, i, vertex_table, tmp_table, radius_table))
	
	cur.execute("insert into %s select distinct dst_id, 0 from %s except (select distinct src_id, 0 from %s)" % (radius_table, edge_table, edge_table))
	conn.commit()
	summarize(conn, radius_table, dataset)
	cur.close()
	conn.close()

