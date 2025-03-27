SELECT * FROM products;

SELECT * FROM products ORDER BY id;

SELECT * FROM products ORDER BY created_at DESC;

SELECT name, price FROM products;

SELECT * FROM products WHERE price>200;

SELECT * FROM products LIMIT 10;

SELECT * FROM products LIMIT 10 OFFSET 2;


INSERT INTO products (name, price, inventory) VALUES ('Shoes', 4, 1000);

INSERT INTO products (name, price, inventory) VALUES ('Bat', 4, 1000) returning *;

DELETE FROM products WHERE id = 25 returning *;

SELECT * from products WHERE inventory = 0;

DELETE FROM products WHERE inventory = 0 RETURNING *;

UPDATE products SET name = 'Watch', price = 50 WHERE id = 1;