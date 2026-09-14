

/* Question 1: Display the information about all customers, sorted alphabetically by their names. */
SELECT *
FROM customers
ORDER BY customerName;

/* Question 2: Display a list of offices sorted by country, state and city.*/

SELECT * 
FROM offices
ORDER BY country, state, city ;

/* Question 3: List the product lines that contain 'Cars' in their name(ignore the case). */

SELECT productLine
FROM products
WHERE LOWER(productLine) LIKE '%cars%';

/* Question 4: Report all the payments made before October 28, 2004.*/

SELECT *
FROM payments 
WHERE paymentDate < '2004-10-28';

/* Question 5: Report those payments that are greater than $100,000 (ignore the $ while writing the query).*/

SELECT *
FROM payments
WHERE amount > 100000;

/* Question 6: Display the name and city of customers who don't have a sales representative? */

SELECT c.customerName AS name, c.city
FROM customers AS c
WHERE c.salesRepEmployeeNumber IS NULL;

/* Question 7: What are the names of executives with VP or Manager (not case sensitive) in their title? Use the
CONCAT function to combine the employee's first name and last name into a single field called
EmployeeName for reporting.*/

SELECT CONCAT(e.firstName, ' ', e.lastName) AS EmployeeName
FROM employees AS e
WHERE LOWER(e.jobtitle) LIKE 'vp%' OR LOWER(e.jobtitle) LIKE '%manager%';

/* Qustion 8: List the names of employees called Dianne or Diane as their first name.*/
SELECT firstName 
FROM employees 
WHERE firstName IN ('Diane', 'Dianne');

/* Question 9: List the name of products with a product code beginning with S700 having buyPrice greater than
60.*/

SELECT productName
FROM products
WHERE productCode LIKE 'S700%' AND buyPrice > 60;

/* Question 10: List all products where quantity in stock is greater than 5000 and less than 8000.*/

SELECT *
FROM products 
WHERE quantityInStock BETWEEN 5000 AND 8000;

/* Question 11: List of all customers who live in ‘Paris’ city. */

SELECT *
FROM customers 
WHERE city = 'Paris';

/* Question 12: Print the order number for all orders placed in the first 6 months of 2005.*/

SELECT orderNumber
FROM orders
WHERE orderDate BETWEEN '2005-01-01' AND '2005-06-30';

/* Question 13: List all the orders that are ‘On Hold’.*/

SELECT *
FROM orders 
WHERE status = 'On Hold';

/* Question 14: Print the name of all customers (customer name as Name and contactLastName +
contactFirstName as Contact) who live in Denmark, Norway, and Sweden.*/

SELECT customerName AS Name, CONCAT(contactLastName, ' ', contactFirstName) AS Contact
FROM customers
WHERE country IN ('Denmark', 'Norway', 'Sweden');

/* Question 15: List all the products (name , vendor and description) where the manufacturer’s suggested retail
price(MSRP) is more than 80 % of the buying price.*/

SELECT productName, productVendor, productDescription
FROM products
WHERE MSRP > (buyPrice*0.8);
