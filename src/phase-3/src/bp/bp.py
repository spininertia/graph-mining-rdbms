import psycopg2
import sys

def time_it(fn):
	def wrapped(*args):
		import time
		start = time.time()
		fn(*args)
		used = time.time() - start
		print "%s used %s" % (str(fn), used)
	return wrapped

@time_it
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

def out_degree(conn, edge_table, degree_table, weighted):
	cur = conn.cursor()
	drop_if_exists(conn, degree_table)
	cur.execute("create table %s(id int, degree int)" % degree_table)
	if weighted == False:
		cur.execute("insert into %s select src_id, count(*) from %s group by src_id" % (degree_table, edge_table))
	else:
		cur.execute("insert into %s select src_id, sum(weight) from %s group by src_id" % (degree_table, edge_table))		
	conn.commit()
	cur.close()

@time_it
def vector_add(conn, m1, m2):
	'''
	result is updated to m1
	'''
	cur = conn.cursor()
	#cur.execute('update %s set val = A.val + B.val from %s as A, %s as B where A.id = B.id' %(m1, m1, m2))
	cur.execute('delete from tmp');
	cur.execute('insert into tmp select A.id, A.val + B.val from %s as A, %s as B where A.id = B.id' % (m1, m2))
	cur.execute('delete from %s' % m1)
	cur.execute('insert into %s select * from tmp' % m1)
	conn.commit()
	cur.close()

def create_vector(conn, tbl_name):
	cur = conn.cursor()
	drop_if_exists(conn, tbl_name)
	cur.execute('create table %s(id int, val float)' % tbl_name)
	conn.commit()

@time_it
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
			if rnd_val > 0.95 then
				retval = 0.001;
			elsif rnd_val < 0.05 then
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

def summarize(conn, final_belief):
	cur = conn.cursor()
	cur.execute("select count(*) from %s where val > 0" % final_belief)
	pos = cur.fetchone()[0]

	cur.execute("select count(*) from %s where val = 0" % final_belief)
	zero = cur.fetchone()[0]

	cur.execute("select count(*) from %s where val < 0" % final_belief)
	neg = cur.fetchone()[0]
	print "postive: %d" % pos
	print "zero: %d" % zero
	print "negative: %d" % neg



def compute_bp(conn, edge_table, target_table, weighted = False):
	create_rnd_init(conn);
	cur = conn.cursor()
	h = 0.002
	a = 4.0 * (h ** 2) / (1 - 4 * h ** 2)
	c = 2.0 * h / (1 - 4 * h ** 2)
	W = "W"
	#W_new = "W_new"
	prior = "prior"
	belief = "bp_" + target_table
	belief_new = "belief_new"
	degree_table = "degree_table"
	out_degree(conn, edge_table, degree_table, weighted)
	create_matrix(conn, W)
	#create_matrix(conn, W_new)
	create_vector(conn, belief)
	create_vector(conn, belief_new)
	create_vector(conn, prior)
	create_vector(conn, 'tmp')
	rand_init_matrix(conn, prior, edge_table)
	if weighted == True:
		cur.execute("insert into %s select src_id, dst_id, weight * %f from %s" % (W, c, edge_table))
	else:
		cur.execute("insert into %s select src_id, dst_id, %f from %s" % (W, c, edge_table))
	conn.commit()
	 
	cur.execute("insert into %s select id, id, -%f * degree from %s" % (W, a, degree_table))
	cur.execute("drop index if exists  w_index")
	cur.execute("create index w_index on %s(col)" % W)
	cur.execute("drop index if exists prior_index");
	cur.execute("create index prior_index on %s(id)" % prior)
	conn.commit()


	print "initialized"
	matrix_vector_multiply(conn, W, prior, belief)

	max_iteration = 10	
	for i in range(max_iteration):
		print "iteration %d" % i
		#cur.execute("delete from %s" % W_new)
		matrix_vector_multiply(conn, W, belief, belief_new)
		vector_add(conn, belief_new, prior)
		if(is_stablized(conn, belief, belief_new)):
			break
		cur.execute("delete from %s" % belief)
		cur.execute("insert into %s select * from %s" % (belief, belief_new))
        conn.commit()

	summarize(conn, belief)


if __name__ == "__main__":
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    compute_bp(conn, sys.argv[1], sys.argv[2])
    conn.close()


