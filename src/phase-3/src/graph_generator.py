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

