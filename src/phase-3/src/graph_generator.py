import random

from common.basic_operation import *

def generate_directed_graph(name, dim, conn):
    """ generate a pseudot random graph """
    cur = conn.cursor()
    drop_if_exists(name, conn)
    cur.execute("create table %s (from_id int, to_id int, value real)" % name)
    for i in range(5, dim):
        cands = set(random.sample(xrange(i), 5))
        for f in cands:
            cur.execute("insert into %s values (%s, %s, %s)" % (name, f, i, random.random()))

def generate_undirected_graph(name, dim, conn):
    """ generate a pseudot undirected random graph """
    cur = conn.cursor()
    drop_if_exists(name, conn)
    cur.execute("create table %s (src_id int, dst_id int, weight float)" % name)
    for i in range(5, dim):
        cands = set(random.sample(xrange(i), 5))
        for f in cands:
            cur.execute("insert into %s values (%s, %s, %s)" % (name, f, i, random.random()))
    cur.execute("insert into %s ((select dst_id, src_id, weight from %s) except (select src_id, dst_id, weight from %s))" % (name, name, name))
    conn.commit()

