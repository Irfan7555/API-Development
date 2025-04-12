import psycopg2
from psycopg2.extras import RealDictCursor
import time
while True:
    try:
        conn = psycopg2.connect(host="localhost",database="postgres",user="postgres",password="789456123", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database")
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        print(posts)
        
        break
    except Exception as e:
        print(f"I am unable to connect to the database: {e}")
        time.sleep(3)

