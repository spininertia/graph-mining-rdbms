def indis(tbl_name, conn):
    """ in degree distribution"""
    pass

def outdis(tbl_name, conn):    
    """ out degree distribution """
    pass

def undirect_dis(tbl_name, result, conn):    
    """ degree distribution """
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % result)
    cur.execute("create table %s(deg int, cnt int)" % result)
    cur.execute("INSERT into %s SELECT degree, count(*) \
                 FROM ( SELECT count(*) as degree FROM %s GROUP BY from_id ) as degree \
                 GROUP BY degree order by degree ASC" % (result, tbl_name))
    conn.commit()