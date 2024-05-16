SELECT * 
FROM sales_item 
WHERE discount > .15
ORDER BY discount DESC;

SELECT time_order_taken
FROM sales_order
WHERE time_order_taken > '2018-12-01' AND time_order_taken <'2018-12-31';

