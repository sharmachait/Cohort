SELECT * 
FROM sales_item 
WHERE discount > .15
ORDER BY discount DESC;

SELECT time_order_taken
FROM sales_order
WHERE time_order_taken > '2018-12-01' AND time_order_taken <'2018-12-31';

SELECT CONCAT(first_name,' ',last_name) AS name
FROM sales_person;

SELECT product_id,SUM(price) FROM item WHERE product_id = 1 GROUP BY product_id ;

SELECT EXTRACT(MONTH FROM birth_date) from customer;

SELECT EXTRACT(MONTH FROM birth_date) AS Month, COUNT(id) 
FROM sales_person 
GROUP BY EXTRACT(MONTH FROM birth_date);

SELECT EXTRACT(MONTH FROM birth_date) AS Month, COUNT(id) 
FROM sales_person 
GROUP BY EXTRACT(MONTH FROM birth_date)
HAVING EXTRACT(MONTH FROM birth_date) <> 12;

SELECT EXTRACT(MONTH FROM birth_date) AS Month, COUNT(id) 
FROM sales_person 
WHERE EXTRACT(MONTH FROM birth_date) <> 12
GROUP BY EXTRACT(MONTH FROM birth_date);