import query

def calculatepagerank(graph, rank, conn):
    cur = conn.cursor()
    cur.execute("drop function if exists calc_pagerank()")
    cur.execute(query.rank_function % (rank, rank, graph, graph, rank, rank, graph, graph, graph, "%", rank, rank, rank, rank, rank, rank))
    print "ranking....."
    cur = conn.cursor();
    cur.execute("select calc_pagerank()")
    conn.commit()
    