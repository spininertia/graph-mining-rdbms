from mst import *
import psycopg2
conn = psycopg2.connect(database="mydb", host="127.0.0.1")

def test_mst():
	cur = conn.cursor()
	t = "t"
	drop_if_exists(t, conn)
	cur.execute('create table %s(src_id int, dst_id int, weight float)' % t)
	conn.commit()
	with open('test.dat') as f:
		for line in f:
			tok = line.split()
			cur.execute("insert into %s values(%s, %s, %s)" % (t, tok[0], tok[1], tok[2]))
	mst(conn, t, t)

if __name__ == '__main__':
	test_mst()