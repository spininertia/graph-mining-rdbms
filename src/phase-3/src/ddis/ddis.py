def indis(tbl_name, result, conn):
    """ in degree distribution"""
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % result)
    cur.execute("create table %s(deg int, cnt int)" % result)
    cur.execute("INSERT into %s SELECT degree, count(*) \
                 FROM ( SELECT count(*) as degree FROM %s GROUP BY to_id ) as degree \
                 GROUP BY degree order by degree ASC" % (result, tbl_name))
    conn.commit()

def outdis(tbl_name, result, conn):    
    """ out degree distribution """
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % result)
    cur.execute("create table %s(deg int, cnt int)" % result)
    cur.execute("INSERT into %s SELECT degree, count(*) \
                 FROM ( SELECT count(*) as degree FROM %s GROUP BY from_id ) as degree \
                 GROUP BY degree order by degree ASC" % (result, tbl_name))
    conn.commit()

def undirect_dis(tbl_name, result, conn):    
    """ degree distribution """
    cur = conn.cursor()
    cur.execute("drop table if exists %s" % result)
    cur.execute("create table %s(deg int, cnt int)" % result)
    cur.execute("INSERT into %s SELECT degree, count(*) \
                 FROM ( SELECT count(*) as degree FROM %s GROUP BY from_id ) as degree \
                 GROUP BY degree order by degree ASC" % (result, tbl_name))
    conn.commit()