import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname='pdf_db',
        user='your_user',
        password='your_password',
        host='localhost'
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pdf_documents
                 (id SERIAL PRIMARY KEY,
                  filename TEXT UNIQUE,
                  filepath TEXT,
                  text_content TEXT,
                  processed BOOLEAN DEFAULT FALSE,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()