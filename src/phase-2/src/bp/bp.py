def matrix_vector_multiply(conn, m1, m2, result):
	cur = conn.cursor()
	cur.execute("delete from %s" % result)
	cur.execute("insert into %s select A.row, sum(A.val * B.val) from %s as A, %s as B where A.col = B.id group by A.row" % (result, m1, m2))
	conn.commit()
	cur.close()


def create_matrix(conn, table_name):
	cur = conn.cursor()
	drop_if_exists(conn, table_name)
	cur.execute("create table %s (row int, col int, val float)" % table_name)
	conn.commit()
	cur.close()


def drop_if_exists(conn, table_name):
	cur = conn.cursor()
	cur.execute("drop table if exists %s" % table_name)
	conn.commit()
	cur.close()

def out_degree(conn, edge_table, degree_table):
	cur = conn.cursor()
	drop_if_exists(conn, degree_table)
	cur.execute("create table %s(id int, degree int)" % degree_table)
	cur.execute("insert into %s select src_id, count(*) from %s group by src_id" % (degree_table, edge_table))
	conn.commit()
	cur.close()

def vector_add(conn, m1, m2):
	'''
	result is updated to m1
	'''
	cur = conn.cursor()
	cur.execute('update %s set val = A.val + B.val from %s as A, %s as B where A.id = B.id' %(m1, m1, m2))
	conn.commit()
	cur.close()

def create_vector(conn, tbl_name):
	cur = conn.cursor()
	drop_if_exists(conn, tbl_name)
	cur.execute('create table %s(id int, val float)' % tbl_name)
	conn.commit()

def rand_init_matrix(conn, matrix, edge_table):
	cur = conn.cursor()
	cur.execute('insert into %s select src_id, rnd_prior() from %s group by src_id' % (matrix, edge_table))
	conn.commit()

def is_stablized(conn, belief, belief_new, threshold = 0.000001):
	cur = conn.cursor()
	cur.execute('select sqrt(sum(power(B.val - A.val, 2))) from %s as A, %s as B where A.id = B.id group by A.id' % (belief, belief_new))
	diff = cur.fetchone()[0]
	if diff < threshold:
		return True
	else:
		return False

def create_rnd_init(conn):
	fcn_def = \
		"""
		CREATE or REPLACE function rnd_prior()
		returns float
		AS
		$$
		DECLARE
		retval float := 0;
		rnd_val float;
		BEGIN
			rnd_val = random();
			if rnd_val > 0.9 then
				retval = 0.001;
			elsif rnd_val < 0.1 then
				retval = -0.001;
			end if;
			return retval;
		END;
		$$
		language plpgsql
		"""
	cur = conn.cursor()
	cur.execute(fcn_def)
	conn.commit()


def bp(conn, edge_table):
	create_rnd_init(conn);
	cur = conn.cursor()
	h = 0.002
	a = 4 * (h ** 2) / (1 - 4 * h ** 2)
	c = 2 * h / (1 - 4 * h ** 2)
	W = "W"
	W_new = "W_new"
	prior = "prior"
	belief = "belief"
	belief_new = "belief_new"
	degree_table = "degree_table"
	out_degree(conn, edge_table, degree_table)
	create_matrix(conn, W)
	create_matrix(conn, W_new)
	create_vector(conn, belief)
	create_vector(conn, belief_new)
	create_vector(conn, prior)
	rand_init_matrix(conn, prior, edge_table)
	cur.execute("insert into %s select src_id, dst_id, %f from %s" % (W, c, edge_table))
	conn.commit()

	cur.execute("insert into %s select id, id, -%f * degree + 1 from %s" % (W, a, degree_table))
	matrix_vector_multiply(conn, W, prior, belief)

	max_iteration = 5
	for i in range(max_iteration):
		print "iteration %d" % i
		cur.execute("delete from %s" % W_new)
		matrix_vector_multiply(conn, W, belief, belief_new)
		vector_add(conn, belief_new, prior)
		if(is_stablized(conn, belief, belief_new)):
			break
		cur.execute("delete from %s" % belief)
		cur.execute("insert into %s select * from %s" % (belief, belief_new))


