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
# 