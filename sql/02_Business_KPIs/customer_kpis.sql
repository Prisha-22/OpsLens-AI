/*=========================================================
CUSTOMER KPIs
=========================================================*/

-----------------------------------------------------------
-- KPI 1 : Total Customers
-----------------------------------------------------------
-- Business KPI:
-- Total number of registered customers.

SELECT
COUNT(*) AS total_customers
FROM customers;


-----------------------------------------------------------
-- KPI 2 : Average Orders per Customer
-----------------------------------------------------------
-- Business KPI:
-- Measures customer engagement.

SELECT
ROUND(AVG(total_orders),2)
AS avg_orders_per_customer
FROM customers;


-----------------------------------------------------------
-- KPI 3 : Premium Membership Percentage
-----------------------------------------------------------
-- Business KPI:
-- Percentage of Premium customers.

SELECT
ROUND(
COUNT(*)*100.0/
(SELECT COUNT(*) FROM customers),
2)
AS premium_percentage
FROM customers
WHERE membership='Premium';


-----------------------------------------------------------
-- KPI 4 : Gold Membership Percentage
-----------------------------------------------------------

SELECT
ROUND(
COUNT(*)*100.0/
(SELECT COUNT(*) FROM customers),
2)
AS gold_percentage
FROM customers
WHERE membership='Gold';


-----------------------------------------------------------
-- KPI 5 : Normal Membership Percentage
-----------------------------------------------------------

SELECT
ROUND(
COUNT(*)*100.0/
(SELECT COUNT(*) FROM customers),
2)
AS normal_percentage
FROM customers
WHERE membership='Normal';


-----------------------------------------------------------
-- KPI 6 : Most Active Customer
-----------------------------------------------------------

SELECT
customer_name,
total_orders
FROM customers
ORDER BY total_orders DESC
LIMIT 1;


-----------------------------------------------------------
-- KPI 7 : Average Customers per City
-----------------------------------------------------------

SELECT
ROUND(AVG(customer_count),2)
FROM
(
SELECT
city,
COUNT(*) AS customer_count
FROM customers
GROUP BY city
)t;