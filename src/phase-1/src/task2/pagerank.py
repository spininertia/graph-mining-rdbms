import psycopg2

# get db connection
conn = psycopg2.connect(database="pagerank", host="127.0.0.1")

# Open a cursor to perform database operations
cur = conn.cursor()

def calculatepagerank(cur, conn, iterations=20):
    # clear out the current PageRank tables
    cur.execute("DROP TABLE IF EXISTS pagerank")
    cur.execute("CREATE TABLE pagerank(nodeid int primary key, score real)")
    cur.execute("CREATE INDEX prankidx ON pagerank(nodeid)")

    # initialize every url with a PageRank of 1.0
    cur.execute("INSERT INTO pagerank select src_id,1.0 from pagerank")
    cur.execute("INSERT INTO pagerank select dst_id,1.0 from pagerank")
    conn.commit()

    for i in range(iterations):
        print "Iteration %d" % i
        for (nodeid,) in cur.execute("SELECT nodeid FROM pagerank"):
            pr = 0.15

            # Loop through all the pages that link to this one
            for (linker,) in cur.execute("SELECT distinct src_id FROM edge WHERE dst_id=%d" % nodeid):
                # Get the PageRank of the linker
                linkingpr=cur.execute("SELECT score FROM pagerank WHERE nodeid=%d" % linker).fetchone()[0]

                # Get the total number of links from the linker
                linkingcount=cur.execute("SELECT count(*) FROM edge WHERE src_id=%d" % linker).fetchone()[0]

                pr+=0.85*(linkingpr/linkingcount)

            cur.execute("update pagerank set score=%f WHERE nodeid=%d" % (pr,nodeid))
        conn.commit()

if __name__ == '__main__':
    calculatepagerank(cur, conn)