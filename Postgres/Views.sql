CREATE VIEW purchase_order_overview AS 
SELECT 
		sales_order.purchase_order_number, 
		customer.company,
		sales_item.quantity,
		product.supplier,
		product.name,
		item.price