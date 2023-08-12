import psycopg2



def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS Phone;
        DROP TABLE IF EXISTS Client CASCADE;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Client(
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(60) NOT NULL,
        last_name VARCHAR(60) NOT NULL,
        email VARCHAR(60) NOT NULL UNIQUE);
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone(
		number TEXT [] UNIQUE,
		number_id INTEGER REFERENCES client(client_id));
        """)
        conn.commit()


def add_client(conn, first_name, last_name, email, number=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Client(first_name, last_name, email)
        VALUES(%s, %s, %s)
        RETURNING client_id, first_name, last_name, email;
        """, (first_name, last_name, email))
        return cur.fetchall()

def add_phone(conn, number_id, number):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Phone (number_id, number)
        VALUES(%s, %s)
        RETURNING number_id, number;
        """, (number_id, number))
        return cur.fetchall()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE Client SET first_name=%s, last_name=%s, email=%s 
        WHERE client_id=%s
        RETURNING client_id, first_name, last_name, email;
        """, (first_name, last_name, email, client_id))
        return cur.fetchone()

def change_phone(conn, number_id, number):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE Phone SET number=%s
        WHERE number_id=%s
        RETURNING number_id, number;
        """, (number, number_id))
        return cur.fetchone()


def delete_phone(conn, number_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Phone
        WHERE number_id=%s;
        """, (number_id))
        cur.execute("""
        SELECT * FROM Phone
        WHERE number_id =%s;
        """, number_id)
        return cur.fetchone()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT Client.first_name, Client.last_name, Client.email, Phone.number FROM Client
        LEFT JOIN PHONE ON Client.client_id = Phone.number_id
        WHERE client_id=%s;
        """, (client_id))
        cur.execute("""
        DELETE FROM Phone
        WHERE number_id=%s;
        """, (client_id))
        cur.execute("""
        DELETE FROM Client
        WHERE client_id=%s;
        """, (client_id))
        cur.execute("""
        SELECT * FROM Client
        WHERE client_id=%s;
        """, (client_id))
        return cur.fetchone()

def find_client(conn, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT Client.first_name, Client.last_name, Client.email, Phone.number FROM Client
        LEFT JOIN Phone ON Client.client_id = Phone.number_id
        WHERE Client.first_name=%s OR Client.last_name=%s OR Client.email=%s OR Phone.number=%s;
        """, (first_name, last_name, email, number))
        return cur.fetchall()


if __name__ == '__main__':
    with psycopg2.connect(database="hw_db_3", user="postgres", password="") as conn:
        print(create_db(conn))
        print(add_client(conn, 'Sarah', 'Valcech', 'salcech@gmail.com'))
        print(add_client(conn, 'Liza', 'Crowley', 'crows@gmail.com'))
        print(add_client(conn, 'Sam', 'Honas', 'sonas@gmail.com'))
        print(add_phone(conn, '1', ['89316495782', '89316495782']))
        print(add_phone(conn, '2', ['89132598765']))
        print(add_phone(conn, '3', ['89315065965', '89412784517']))
        print(change_client(conn, '1', 'Vera', 'Samoylova', 'velova@gmail.com'))
        print(change_phone(conn, '1', ['89215487253']))
        print(delete_phone(conn, '2'))
        print(delete_client(conn, '1'))
        print(find_client(conn, 'Sam'))
        conn.commit()

conn.close()