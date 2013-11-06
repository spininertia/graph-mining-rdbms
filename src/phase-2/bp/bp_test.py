import bp
import psycopg2

conn = psycopg2.connect(database="mydb", host="127.0.0.1")
if __name__ == '__main__':
	bp.bp(conn, "edge")
