CREATE TABLE customer(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    birth_date DATE NULL,
    date_entered TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	email VARCHAR(60) NOT NULL,
	company VARCHAR(60) NOT NULL,
	street VARCHAR(50) NOT NULL,
	city VARCHAR(40) NOT NULL,
	state CHAR(2) NOT NULL,
	zip SMALLINT NOT NULL,
	phone VARCHAR(20) NOT NULL,
	sex CHAR(1) NOT NULL
);

INSERT INTO customer
	(first_name,
	last_name, 
	email, 
	company, 
	street, 
	city, 
	state, 
	zip, 
	phone, 
	birth_date, 
	sex, 
	date_entered) 
VALUES 
	('Christopher', 
	'Jones', 
	'christopherjones@bp.com', 
	'BP', 
	'347 Cedar St', 
	'Lawrenceville', 
	'GA', 
	'30044', 
	'348-848-8291', 
	'1938-09-11', 
	'M', 
	current_timestamp);

SELECT * FROM sales_db.public.customer;

CREATE TYPE sex_type as enum ('M','F');

DELETE FROM customer
WHERE id=1;

ALTER TABLE customer
ALTER COLUMN sex TYPE sex_type USING sex::sex_type;

DROP TABLE customer;

DROP TYPE sex;

CREATE TABLE sales_person(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    birth_date DATE NULL,
    date_hired TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	email VARCHAR(60) NOT NULL,
	company VARCHAR(60) NOT NULL,
	street VARCHAR(50) NOT NULL,
	city VARCHAR(40) NOT NULL,
	state CHAR(2) NOT NULL DEFAULT 'PA',
	zip SMALLINT NOT NULL,
	phone VARCHAR(20) NOT NULL,
	sex sex_type NOT NULL
);

CREATE TABLE product_type(
	id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE product(
	id SERIAL PRIMARY KEY,
	type_id INTEGER REFERENCES product_type(id),
	name VARCHAR(30) NOT NULL,
	supplier VARCHAR(30) NOT NULL,
	description TEXT NOT NULL
);

CREATE TABLE item(
	id SERIAL PRIMARY KEY,
	product_id INTEGER REFERENCES product(id),
	size INTEGER NOT NULL,
	color VARCHAR(30) NOT NULL,
	picture VARCHAR(256) NOT NULL,
	price NUMERIC(6,2) NOT NULL
);

CREATE TABLE sales_order(
	id SERIAL PRIMARY KEY,
	cust_id INTEGER REFERENCES customer(id),
	sales_person_id INTEGER REFERENCES sales_person(id),
	time_order_taken TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	purchase_orer_number INTEGER NOT NULL,
	credit_card_number VARCHAR(16) NOT NULL,
	credit_card_exper_month SMALLINT NOT NULL,
	credit_card_exper_day SMALLINT NOT NULL,
	credit_card_secret_code SMALLINT NOT NULL,
	name_on_card VARCHAR(100) NOT NULL
);

CREATE TABLE sales_item(
	item_id INTEGER REFERENCES item(id),
	sales_order_id INTEGER REFERENCES sales_order(id),
	quantity INTEGER NOT NULL,
	discount NUMERIC(3,2) NULL DEFAULT 0,
	taxable BOOLEAN NOT NULL DEFAULT FALSE,
	sales_tax_rate NUMERIC(5,2) NOT NULL DEFAULT 0,
	id SERIAL PRIMARY KEY
);

ALTER TABLE sales_item ADD day_of_week VARCHAR(8)

ALTER TABLE sales_item ALTER COLUMN day_of_week SET NOT NULL;

ALTER TABLE sales_item ADD items_id INTEGER REFERENCES item(id) ON DELETE CASCADE;

ALTER TABLE saLes_item DROP COLUMN items_id;

ALTER TABLE sales_item RENAME COLUMN day_of_week TO weekday;

ALTER TABLE sales_item DROP COLUMN weekday;


CREATE TABLE transaction_type(
	name VARCHAR(30) NOT NULL,
	payment_type VARCHAR(30) NOT NULL,
	id SERIAL PRIMARY KEY
);

ALTER TABLE transaction_type RENAME TO transaction;

CREATE INDEX transaction_id ON transaction(name)

CREATE INDEX transaction_id_2 ON transaction(name, payment_type)

TRUNCATE TABLE transaction
 
DROP TABLE transaction

DROP INDEX transaction_id;

DROP INDEX transaction_id_2;










