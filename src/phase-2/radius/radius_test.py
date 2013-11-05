import psycopg2
from radius import radius
from functions import init_user_defined_funcs
conn = psycopg2.connect(database="mydb", host="127.0.0.1")

if __name__ == '__main__':
	init_user_defined_funcs(conn)
	radius("edge", conn)