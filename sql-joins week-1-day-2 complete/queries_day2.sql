-- =========================================================
-- Cynaris Internship
-- Week 1 - Day 2
-- SQL Joins - Combining Tables
-- =========================================================

USE cynaris_day1;


-- =========================================================
-- 1. CREATE CUSTOMERS TABLE
-- =========================================================

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    city VARCHAR(100)
);

INSERT INTO customers (customer_id, customer_name, city)
VALUES
(1, 'Rahul', 'Bangalore'),
(2, 'Priya', 'Mumbai'),
(3, 'Amit', 'Delhi'),
(4, 'Neha', 'Pune'),
(5, 'Rohan', 'Ahmedabad');


-- =========================================================
-- 2. INNER JOIN
-- Show only records that match in both tables
-- =========================================================

SELECT
    s.sale_id,
    s.customer_name,
    s.product,
    s.amount,
    c.city AS customer_city
FROM sales s
INNER JOIN customers c
    ON s.customer_name = c.customer_name;


-- =========================================================
-- 3. LEFT JOIN
-- Show all sales, including sales whose customer
-- is not found in the customers table
-- =========================================================

SELECT
    s.sale_id,
    s.customer_name,
    s.product,
    s.amount,
    c.city AS customer_city
FROM sales s
LEFT JOIN customers c
    ON s.customer_name = c.customer_name;


-- =========================================================
-- 4. RIGHT JOIN
-- Show all customers, including customers
-- who have no matching sales
-- =========================================================

SELECT
    s.sale_id,
    s.customer_name,
    s.product,
    s.amount,
    c.city AS customer_city
FROM sales s
RIGHT JOIN customers c
    ON s.customer_name = c.customer_name;


-- =========================================================
-- 5. FULL OUTER JOIN
-- MySQL does not support FULL OUTER JOIN directly.
-- This UNION gives the FULL OUTER JOIN result.
-- =========================================================

SELECT
    s.sale_id,
    s.customer_name,
    s.product,
    s.amount,
    c.city AS customer_city
FROM sales s
LEFT JOIN customers c
    ON s.customer_name = c.customer_name

UNION

SELECT
    s.sale_id,
    s.customer_name,
    s.product,
    s.amount,
    c.city AS customer_city
FROM customers c
LEFT JOIN sales s
    ON s.customer_name = c.customer_name;


-- =========================================================
-- 6. DUPLICATE ROWS CAUSED BY JOIN
-- A customer can have multiple sales.
-- This demonstrates a one-to-many relationship.
-- =========================================================

SELECT
    c.customer_name,
    s.sale_id,
    s.product,
    s.amount
FROM customers c
INNER JOIN sales s
    ON c.customer_name = s.customer_name;


-- =========================================================
-- 7. HANDLE DUPLICATES
-- Aggregate sales so that each customer appears once.
-- =========================================================

SELECT
    c.customer_name,
    COUNT(s.sale_id) AS total_sales,
    SUM(s.amount) AS total_amount
FROM customers c
LEFT JOIN sales s
    ON c.customer_name = s.customer_name
GROUP BY c.customer_name;


-- =========================================================
-- 8. CREATE EMPLOYEES TABLE FOR SELF JOIN
-- =========================================================

DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    manager_id INT
);

INSERT INTO employees (employee_id, employee_name, manager_id)
VALUES
(1, 'Raj', NULL),
(2, 'Rahul', 1),
(3, 'Priya', 1),
(4, 'Amit', 2);


-- =========================================================
-- 9. SELF JOIN
-- Find each employee and their manager.
-- =========================================================

SELECT
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e
LEFT JOIN employees m
    ON e.manager_id = m.employee_id;