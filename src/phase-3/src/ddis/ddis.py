def indis(tbl_name, conn):
    """ in degree distribution"""
    pass

def outdis(tbl_name, conn):    
    """ out degree distribution """
    pass

def undirect_dis(tbl_name, result, conn):    
    """ degree distribution """
    cur = conn.cursor()
    cur.execute("INSERT into %s SELECT degree, count(*) \
                 FROM ( SELECT count(*) as degree FROM %s GROUP BY from_id ) as degree \
                 GROUP BY degree order by degree DESC")
    cur.commit()