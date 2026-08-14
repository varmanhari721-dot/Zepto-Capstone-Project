-- Query 1: SELECT / WHERE / BETWEEN / ORDER BY
SELECT title, price_gbp, rating, in_stock
FROM books
WHERE in_stock = 1
  AND price_gbp BETWEEN 10 AND 20
ORDER BY price_gbp ASC;

-- Query 2: ORDER BY / LIMIT
SELECT title, price_gbp, rating
FROM books
ORDER BY price_gbp DESC
LIMIT 10;

-- Query 3: DISTINCT / JOIN
SELECT DISTINCT c.category_name
FROM categories AS c
JOIN books AS b
    ON c.category_id = b.category_id
ORDER BY c.category_name;

-- Query 4: IN
SELECT title, rating, price_gbp
FROM books
WHERE rating IN (4, 5)
ORDER BY rating DESC, price_gbp DESC;

-- Query 5: JOIN
SELECT
    c.category_name,
    b.title,
    b.rating,
    b.price_gbp,
    b.price_inr
FROM books AS b
JOIN categories AS c
    ON b.category_id = c.category_id
WHERE b.rating = (
    SELECT MAX(b2.rating)
    FROM books AS b2
    WHERE b2.category_id = b.category_id
)
ORDER BY c.category_name, b.title;