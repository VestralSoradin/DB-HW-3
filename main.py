import psycopg2

conn = psycopg2.connect(database="hw_db_3", user="postgres", password="")


def create_db(conn):
    with conn.cursor() as cur:
        # cur.execute("""
        #	DROP TABLE Phone;
        #	DROP TABLE Client;
        #	""")

        cur.execute("""
			CREATE TABLE IF NOT EXISTS client(
			id SERIAL PRIMARY KEY,
			name VARCHAR(60) NOT NULL,
			lastname VARCHAR(60) NOT NULL,
			email VARCHAR(60) NOT NULL UNIQUE
			);
			""")
        conn.commit()

        cur.execute("""
			CREATE TABLE IF NOT EXISTS phone(
			number INTEGER UNIQUE CHECK (number <= 99999999999),
			phone_id INTEGER REFERENCES client(client_id)
			);
			""")
        conn.commit()


def add_client(conn, name, lastname, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
			INSERT INTO client (name, lastname, email)
			VALUES (name, lastname, email)
			RETURNING client_id, name, lastname, email;
			""")
    print(cur.fetchone())


def add_phone(conn, phone_id, number):
    with conn.cursor() as cur:
        cur.execute("""
			INSERT INTO Phone (number, phone_id)
			VALUES (number, phone_id)
			RETURNING phone_id, name, lastname, email;
			""")
    print(cur.fetchone())


def change_client(conn, client_id, name=None, lastname=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
			UPDATE client
			SET name=%s, lastname=%s, email=%s;
			WHERE id=%s
			RETURNING client_id, name, lastname, email;
			""", (name, lastname, email,))
    print(cur.fetchone())


def change_phone(conn, client_id, name=None, lastname=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
			UPDATE phone
			SET number=%s;
			WHERE phone_id=%s
			RETURNING phone_id, number;
			""", (number,))
    print(cur.fetchone())


def delete_phone(conn, phone_id, number):
    with conn.cursor() as cur:
        cur.execute("""
			DELETE FROM phone
			WHERE phone_id=%s;
			""", (phone_id,))
    print(cur.fetchall())


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
			DELETE FROM client
			WHERE client_id=%s;
			""", (client_id,))
    print(cur.fetchall())


def find_client(conn, name=None, lastname=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
			SELECT client.name, client.lastname, client.email, phone.number From client
			LEFT JOIN hhone ON client.client_id = phone.phone_id
			WHERE c.name=%s OR c.lastname=%s OR c.email=%s OR p.number=%s;
			""", (name, lastname, email, number,))
    return cur.fetchone()[0]


print(create_db(conn))
print(add_client(conn, 'Sarah', 'Valcech', 'salcech@gmail.com'))
print(add_phone(conn, '1', '89316495782'))
print(change_client(conn, '1', 'Liza', 'Crowley', 'crows@gmail.com'))
print(delete_phone(conn, '1', '89316495782'))
print(delete_client(conn, '1'))
print(find_client(conn, 'Liza'))

conn.close()
