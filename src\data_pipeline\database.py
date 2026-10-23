"""Transactional PostgreSQL persistence for valid fixtures."""

def persist(database_url, customers, orders):
    import psycopg
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY, name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE, age INTEGER NOT NULL CHECK(age BETWEEN 18 AND 120),
                country CHAR(2) NOT NULL)""")
            cur.execute("""CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL REFERENCES customers(customer_id),
                amount NUMERIC(12,2) NOT NULL CHECK(amount > 0))""")
            cur.executemany("INSERT INTO customers VALUES (%(customer_id)s,%(name)s,%(email)s,%(age)s,%(country)s) ON CONFLICT DO NOTHING", customers)
            cur.executemany("INSERT INTO orders VALUES (%(order_id)s,%(customer_id)s,%(amount)s) ON CONFLICT DO NOTHING", orders)
        conn.commit()

