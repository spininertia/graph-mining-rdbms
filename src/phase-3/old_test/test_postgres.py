import sys
import time
import psycopg2

if __name__ == "__main__" :
    conn = psycopg2.connect(database="mydb", host="127.0.0.1", user="postgres")
    print "Testing postgres."