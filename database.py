import psycopg2
from psycopg2 import sql

def create_connection():
    return psycopg2.connect(
        dbname="my_dog_project",
        user="daniela",
        password="daniela123",
        host="localhost",
        port="5432"
    )

def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dog_images (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_url(url):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO dog_images (url) VALUES (%s)", (url,))
    conn.commit()
    cur.close()
    conn.close()
