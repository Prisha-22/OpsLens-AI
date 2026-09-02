/*=========================================================
CUSTOMER ANALYSIS
=========================================================*/

-----------------------------------------------------------
-- 1. Total Customers
-----------------------------------------------------------
-- Business Question:
-- How many customers are registered on the platform?
--
-- Insight:
-- Shows the total size of the customer base.

SELECT COUNT(*) AS total_customers
FROM customers;


-----------------------------------------------------------
-- 2. Customers by Membership
-----------------------------------------------------------
-- Business Question:
-- Which membership plan is the most popular among customers?
--
-- Insight:
-- Helps understand customer preference for different
-- membership plans and supports marketing decisions.

SELECT
    membership,
    COUNT(*) AS total_customers
FROM customers
GROUP BY membership
ORDER BY total_customers DESC;


-----------------------------------------------------------
-- 3. Customers by City
-----------------------------------------------------------
-- Business Question:
-- Which cities have the highest number of customers?
--
-- Insight:
-- Identifies cities with the largest customer base for
-- expansion and promotional campaigns.

SELECT
    city,
    COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY customers DESC;


-----------------------------------------------------------
-- 4. Average Orders per Customer
-----------------------------------------------------------
-- Business Question:
-- How active are customers on average?
--
-- Insight:
-- Measures customer engagement by calculating the
-- average number of orders placed by each customer.

SELECT
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer
FROM customers;


-----------------------------------------------------------
-- 5. Top 10 Customers
-----------------------------------------------------------
-- Business Question:
-- Who are the most valuable customers based on order activity?
--
-- Insight:
-- Identifies loyal customers who place the highest
-- number of orders and can be targeted for rewards.

SELECT
    customer_name,
    total_orders
FROM customers
ORDER BY total_orders DESC
LIMIT 10;