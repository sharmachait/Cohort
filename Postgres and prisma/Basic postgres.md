# Common definitions
1. Views - a stored query definition that can be used to simplify writing SQL statements or to secure data access, can be thought of as simplified data design to perform queries faster
2. Stored Procedures - stored script that can include queries, DDL to create or modify objects and programming logic. they can return tabular data.
3. User defined functions - similar to stored procedures but can return tabular data as well as single value, cant affect anything outside the function.
4. Indexes - data structure that increases the speed of queries
5. Constraints - rules that govern the behaviors and permissible values of the table and the columns
6. Triggers - special type of stored procedures that fires when something happens in the database like when a row is inserted or when an object is created
7. Sequences - User defined object that generates a sequence of numbers 

# some notes
- each table in a normalized database should hold information about only one type of entity and a primary key.
- each column has a definition specifying a data type along with rules AKA constraints.
- we can have a computed data type where the value of the column is calculated with a formula
![[Pasted image 20240606120107.png]]
- we can have user defined data types as well, like a phone number

# SQL sublanguages
## 1. DDL
- data definition language
- create modify and delete database structures
1. CREATE 
```postgresql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone phone_number
);
```
2. DROP
```SQL
DROP TABLE contacts;
```
3. ALTER
```postgresql
ALTER TABLE contacts
ADD COLUMN address VARCHAR(255);

ALTER TABLE contacts
DROP COLUMN address;

ALTER TABLE contacts
ALTER COLUMN phone TYPE TEXT;

ALTER TABLE contacts
RENAME COLUMN phone TO phone_number;
```
4. TRUNCATE
```postgresql
TRUNCATE TABLE contacts;
```
## 2. DQL
- data query language
1. SELECT
## 3. DML
- data manipulation language
1. INSERT
```postgresql
INSERT INTO contacts (name, phone, email)
VALUES ('John Doe', '555-5555', 'johndoe@example.com');
```
2. UPDATE
```postgresql
UPDATE contacts
SET email = 'john.doe@example.com'
WHERE id = 1;
```
3. DELETE
```postgresql
DELETE FROM contacts
WHERE id = 1;
```
## 4. DCL
- data control language, used for privileges
1. GRANT
2. REVOKE
## 5. TCL
- transaction control language
1. BEGIN TRANSACTION
2. COMMIT
3. ROLLBACK
# custom data types 
```sql
CREATE TYPE phone_number AS (
    country_code VARCHAR(5),
    area_code VARCHAR(5),
    number VARCHAR(15)
);

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone phone_number
);

INSERT INTO contacts (name, phone) VALUES 
('John Doe', ROW('+1', '800', '5551234')),
('Jane Smith', ROW('+44', '20', '79460000'));

SELECT 
    name, 
    phone.country_code, 
    phone.area_code, 
    phone.number 
FROM contacts;
```
# enums
```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');

CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    current_mood mood
);

-- Insert data
INSERT INTO person (name, current_mood) VALUES ('Alice', 'happy'), ('Bob', 'sad');

-- Query data
SELECT name, current_mood FROM person;

```
# Indexes
- everytime we create a key or a unique column we place an index on the column
- indexes are stored separately from the data but accessed automatically when we run a query
- and are updated everytime a row is added or removed from the table
- index is a data structure to help DB look up information fast, usually a balanced tree on data that can be ordered and searched using the equality operators `<,>,<=,>=,==,` and `between`
- its created automatically but we can create it with create index command
- instead of Btrees there are other generalized types of indexes as well

### kinds of indexes
1. clustered
	1. stores and organizes the table
	2. arrange the data in the table like sort to make look up faster
	3. a table can have only one clustered index thats because its just the entire table sorted on the cluster key
	4. when we add new rows old rows dont have to move for them to stay in order because the new row will be added into the correct data page which will have some free space
2. non-clustered
	1. defined on one or more columns of the table, its a separate structure that points to the actual table
	2. stores the data and records in different tables so that scanning records is faster to look for the data you want

indexes are optional but greatly improve performance when properly designed and implemented

but they can also take up disk space

If a table has four nonclustered indexes, every write to that table may require four additional writes to keep the indexes up to date
##### example
- phone directory, primary key is the phone number but the cluster key is the first name plus the last name
- if the name starts with d you start looking in the beginning of the directory in your brain you did this calculation
    - mid alphabet is j or k and d<j or k so it must be in the first half, thats basically a binary search

# Connect to the desired database (equivalent to USE in SQL Server)
```postgresql
\c AdventureWorks2022
```

### *when comparing columns together or to a static values it resolves to true or false and based on that values are returned, but if the column contains null it resolves to UKNOWN instead, and the values are not returned for that either. -  the opposite of false is true but the opposite of UNKNOWN is still UNKNOWN. be weary of always accounting for nulls especially when filtering using the NOT operator. when using "<" operator rows with NULL will be left out*

# built in functions
## concatinating strings
```postgresql
SELECT 'Hello, ' || 'World!' AS greeting;
```
If you need to handle `NULL` values and avoid having them disrupt the concatenation, you can use the `CONCAT` function or the `COALESCE` function to provide a default value:
### concat()
```postgresql
SELECT CONCAT(column1, ' ', column2) AS full_text FROM your_table;
-- or
SELECT COALESCE(column1, '') || ' ' || COALESCE(column2, '') AS full_text FROM your_table;
```

## handling nulls
### coalesce()
takes in any number of inputs and returns the first non-null value
```postgresql
SELECT FirstName +coalesce(concat(' ',MiddleName),'')+' '+LastName AS FullName FROM Person.Person;
```

## casting
### cast()
```sql
SELECT 1 + CAST('1' AS INTEGER);
```
or
```postgresql
SELECT 1 + '1'::INTEGER;

SELECT 1::TEXT || '1';
```

## mathematics
```postgresql
SELECT
    1 + 1 AS ADDITION,
    10.0 / 3 AS DIVISION,
    10 / 3 AS "Integer Division",
    10/3.0 AS "Decimal Division",
    10 % 3 AS MODULO;
```

## string functions
### RTRIM, LTRIM and TRIM functions

```postgresql

SELECT RTRIM('Hello World   ');

SELECT LTRIM('   Hello World');

SELECT TRIM('   Hello World   ');

-- You can also specify the characters to be removed
SELECT RTRIM('Hello Worldxxx', 'x');
SELECT LTRIM('xxxHello World', 'x');
SELECT TRIM('xHello Worldx', 'x');
```

### LEFT, RIGHT and SUBSTRING functions 
```postgresql
-- Extracts the first 5 characters from the left of the string
SELECT LEFT('Hello World', 5);

-- Extracts the last 5 characters from the right of the string
SELECT RIGHT('Hello World', 5);

-- Extracts a substring starting at position 2 for 3 characters
SELECT SUBSTRING('Hello World' FROM 2 FOR 3);

-- we can also perform slicing in postgresql
SELECT 'Hello World'[2:4];
```

### length of string
```postgresql
SELECT LENGTH('Hello World');
```

### index of character of substring
```postgresql
SELECT POSITION('World' IN 'Hello World');
```

### reverse a string
```sql
SELECT REVERSE('Hello World');
```

### upper and lower
```sql
-- Convert to upper case
SELECT UPPER('Hello World');

-- Convert to lower case
SELECT LOWER('Hello World');
```

### replace
```sql
-- Replace 'World' with 'Everyone'
SELECT REPLACE('Hello World', 'World', 'Everyone');
```

## date and time functions