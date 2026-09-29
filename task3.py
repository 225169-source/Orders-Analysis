import sqlite3

# Connect to database
conn = sqlite3.connect("orders.db")
cur = conn.cursor()

# Create tables and insert data
cur.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

INSERT INTO customers VALUES
(1, 'Ali', 'Islamabad'),
(2, 'Sara', 'Lahore'),
(3, 'Bilal', 'Karachi'),
(4, 'Usman', 'Islamabad'),
(5, 'Zainab', 'Lahore'),
(6, 'Hassan', 'Peshawar');

INSERT INTO orders VALUES
(101, 1, 4500), (102, 1, 7200),
(103, 2, 3000), (104, 3, 9800),
(105, 4, 6000), (106, 4, 5500),
(107, 5, 8000), (108, 5, 4000),
(109, 6, 2000), (110, 2, 1500);
""")
conn.commit()

# Query (a): INNER JOIN
print("--- Customer orders (joined) ---")
cur.execute("""
SELECT c.name, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;
""")
for row in cur.fetchall():
    print(row)

# Query (b): Total spend per customer
print("\n--- Total spend per customer ---")
cur.execute("""
SELECT c.name, SUM(o.amount) AS total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spend DESC;
""")
for row in cur.fetchall():
    print(row)

# Query (c): Cities with total spend > 10,000 using HAVING
print("\n--- Cities with total spend > 10,000 ---")
cur.execute("""
SELECT c.city, SUM(o.amount) AS city_total
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING city_total > 10000;
""")
for row in cur.fetchall():
    print(row)

conn.close()
