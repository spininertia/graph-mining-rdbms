import psycopg2
import sys

def drop_if_exists(conn, table_name):
	cur = conn.cursor()
	cur.execute("drop table if exists %s" % table_name)
	conn.commit()
	cur.close()

def cc_init(conn, edge_table, target_table):
	cur = conn.cursor()
	drop_if_exists(conn, "component")
	drop_if_exists(conn, "component_tmp")
	drop_if_exists(conn, target_table)
	cur.execute("drop index if exists c_index")
	cur.execute("drop index if exists ct_index")
	cur.execute("create table component (nid int not null unique, cid int)")
	cur.execute("create table component_tmp (nid int, cid int)")
	cur.execute("create table %s (nid int, cid int)" % target_table)
	cur.execute("insert into component_tmp(nid, cid) select distinct src_id, src_id from %s" % edge_table)
	cur.execute("insert into component_tmp(nid, cid) select distinct dst_id, dst_id from %s" % edge_table)
	cur.execute("""
		insert into component (nid, cid) select distinct nid, cid from component_tmp;
		drop table component_tmp;
		create table component_tmp (nid int, cid int);
		insert into component_tmp (nid, cid) select nid, cid from component;
		create index c_index on component (nid);
		create index ct_index on component_tmp (nid);
		""")
	conn.commit()
	cur.close()

def save_result(conn, target_table):
	cur = conn.cursor()
	cur.execute("insert into %s(nid, cid) select nid, cid from component order by nid" % target_table)
	conn.commit()
	cur.close()

def update(conn, edge_table):
	cur = conn.cursor()
	cur.execute("""
	update component
		set cid = new_cid
		from (
			select dst_id as id, min(component.cid) as new_cid
			from %s, component
			where src_id = component.nid 
			group by id
			) as newComponent
		where nid = id and new_cid < cid;
	""" % edge_table)
	conn.commit()
	cur.execute("""
	update component
		set cid = new_cid
		from (
			select src_id as id, min(component.cid) as new_cid
			from %s, component
			where dst_id = component.nid 
			group by id
			) as newComponent
		where nid = id and new_cid < cid;
	""" % edge_table) 
	conn.commit()
	cur.close()

def count_diff(conn):
	cur = conn.cursor()
	cur.execute("""
		select count(*)
		from component, component_tmp
		where component.nid = component_tmp.nid and component.cid <> component_tmp.cid;
	""")
	diff = cur.fetchone()[0]
	return diff

def cc_assign(conn):
	cur = conn.cursor()
	cur.execute("""
		update component_tmp 
		set cid = ccid
		from (
			select component.nid as nnid, component.cid as ccid
			from component
			) as cmpt
		where nid = nnid;
		""")
	conn.commit()

def summarize(conn, target_table):
	cur = conn.cursor()
	cur.execute("select count(distinct cid) from %s" % target_table)
	num_cc = cur.fetchone()[0]
	cur.execute("select max(cnt) from (select count(*) as cnt from %s group by cid) as foo" % target_table)
	max_cc = cur.fetchone()[0]
	print "number of connected components:%d" % num_cc
	print "largest connected components:%d vertices" % max_cc 
	cur.close()

def compute_cc(conn, edge_table, target_table):
	cc_init(conn, edge_table, target_table)
	update(conn, edge_table)
	diff = count_diff(conn)
	iter = 1
	while diff > 0:
		print "interation %d %d" % (iter, diff)
		cc_assign(conn)
		update(conn, edge_table)
		diff = count_diff(conn)
		iter = iter + 1
	save_result(conn, target_table)
	summarize(conn, target_table)

	
if __name__ == "__main__":
	conn = psycopg2.connect(database="mydb", host="127.0.0.1")
	compute_cc(conn, sys.argv[1], "cc_" + sys.argv[2])
	conn.close()

