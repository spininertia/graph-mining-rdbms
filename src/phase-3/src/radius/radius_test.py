import psycopg2
from radius import radius
from functions import init_udf
import sys

conn = psycopg2.connect(database="mydb", host="127.0.0.1")

if __name__ == '__main__':
	init_udf(conn)
	radius(conn, sys.argv[1], sys.argv[2])