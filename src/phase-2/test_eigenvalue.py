import sys

import psycopg2
from eigenvalue.eigen_quodratic import *
from common.basic_operation import *

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1")
    # prepare data
    clear_table("v", conn)
    cur = conn.cursor()
    cur.execute("insert into %s values (0,0,0.3),(0,1,0.4),(1,0,0.5),(1,1,0.6)" % 'v')
    conn.commit()
    # do quodratic QR method
    eigen_quodratic("v", 'q', 'r', 2, conn)