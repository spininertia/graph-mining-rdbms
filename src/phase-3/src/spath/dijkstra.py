from common.basic_operation import *

select_id_query = '''\
select distinct nid \
from (\
    select from_id from %s \
    union\
    select to_id from %s\
    )\
as nid
'''

def dijkstra(start, graph, result, stamp, conn):
    """ dijksrta algorithm """
    # initilize table
    # 1. Distance (nodeid, distance, mark)
    # 2. Graph (from_id, to_id, value)
    cur = conn.cursor()
    distance = "Distance_%s" % stamp
    drop_if_exists(distance, conn)
    drop_if_exists(result, conn)
    cur.execute("create table %s (nodeid int, distance real, mark boolean)" % distance)
    cur.execute("create table %s (nodeid int, distance real, mark boolean)" % result)
    cur.execute(select_id_query % (graph, graph))
    ids = cur.fetchall()
    # initialize all node's distance
    for i in ids:
        cur.execute("insert into %s values (%s, %s, '%s')" % (distance, i[0], 9999999999, 'f'))
    # make start point best
    cur.execute("update %s set distance = 0 where nodeid = %s" % (distance, start))
    cur.execute("create index nodeindex on %s (nodeid)" % (distance))
    for i in range(len(ids)):        
        cur.execute("select nodeid, distance from %s where mark = 'f' order by distance asc limit 1" % distance)
        candidate = cur.fetchone()
        if candidate[1] == 9999999999:
            break
        if i % 1000 == 0:
            print i, candidate[1]
        cur.execute("update %s set mark = 't' where nodeid = %s" % (distance, candidate[0]))
        cur.execute("select to_id, value from %s,%s where from_id = %s and nodeid = to_id and mark = 'f'" % (distance, graph, candidate[0]))
        neighbours = cur.fetchall()
        # update neighbours
        for nbr in neighbours:
            cur.execute("update %s set distance = %s where distance > %s and nodeid = %s" % (distance, candidate[1]+nbr[1], candidate[1]+nbr[1], nbr[0]))
    assign_to(distance, result, conn)            
    drop_if_exists(distance, conn)
    print "Result is in %s" % result
    conn.commit()