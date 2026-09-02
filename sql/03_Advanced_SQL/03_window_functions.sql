/*=========================================================
WINDOW FUNCTIONS
=========================================================*/

-----------------------------------------------------------
-- 1. Rank Customers by Total Orders
-----------------------------------------------------------
-- Business Question:
-- Who are the most active customers on the platform?
--
-- Insight:
-- Ranks customers based on the total number of orders placed.

SELECT
    customer_name,
    total_orders,
    RANK() OVER(ORDER BY total_orders DESC) AS customer_rank
FROM customers;


-----------------------------------------------------------
-- 2. Dense Rank Restaurants by Rating
-----------------------------------------------------------
-- Business Question:
-- Which restaurants have the highest ratings?
--
-- Insight:
-- Assigns rankings without skipping numbers when there are ties.

SELECT
    restaurant_name,
    rating,
    DENSE_RANK() OVER(ORDER BY rating DESC) AS restaurant_rank
FROM restaurants;


-----------------------------------------------------------
-- 3. Rank Riders by Experience
-----------------------------------------------------------
-- Business Question:
-- Which riders are the most experienced?
--
-- Insight:
-- Helps identify senior delivery partners.

SELECT
    rider_name,
    experience_years,
    RANK() OVER(ORDER BY experience_years DESC) AS rider_rank
FROM riders;


-----------------------------------------------------------
-- 4. Row Number for Orders
-----------------------------------------------------------
-- Business Question:
-- Assign a unique sequence number to every order.
--
-- Insight:
-- Useful for pagination and ordered reporting.

SELECT
    order_id,
    order_value,
    ROW_NUMBER() OVER(ORDER BY order_value DESC) AS row_num
FROM orders;


-----------------------------------------------------------
-- 5. Running Revenue
-----------------------------------------------------------
-- Business Question:
-- How does cumulative revenue grow over time?
--
-- Insight:
-- Shows running total revenue as orders increase.

SELECT
    order_id,
    order_value,
    SUM(order_value)
    OVER(ORDER BY order_time) AS running_revenue
FROM orders;


-----------------------------------------------------------
-- 6. Average Order Value by Customer
-----------------------------------------------------------
-- Business Question:
-- What is the average order value for each customer?
--
-- Insight:
-- Compares customer spending behavior.

SELECT
    customer_id,
    order_value,
    ROUND(
        AVG(order_value)
        OVER(PARTITION BY customer_id),2
    ) AS avg_customer_order
FROM orders;


-----------------------------------------------------------
-- 7. Highest Order in Each Customer Group
-----------------------------------------------------------
-- Business Question:
-- What is the highest-value order placed by each customer?
--
-- Insight:
-- Identifies each customer's biggest purchase.

SELECT
    customer_id,
    order_value,
    MAX(order_value)
    OVER(PARTITION BY customer_id) AS highest_order
FROM orders;


-----------------------------------------------------------
-- 8. Number of Orders per Customer
-----------------------------------------------------------
-- Business Question:
-- How many orders has each customer placed?
--
-- Insight:
-- Displays customer activity using window functions.

SELECT
    customer_id,
    order_id,
    COUNT(*)
    OVER(PARTITION BY customer_id) AS total_orders
FROM orders;


-----------------------------------------------------------
-- 9. Revenue Rank
-----------------------------------------------------------
-- Business Question:
-- Which orders generated the highest revenue?
--
-- Insight:
-- Ranks orders based on order value.

SELECT
    order_id,
    order_value,
    DENSE_RANK()
    OVER(ORDER BY order_value DESC) AS revenue_rank
FROM orders;


-----------------------------------------------------------
-- 10. Delivery Time Ranking
-----------------------------------------------------------
-- Business Question:
-- Which deliveries took the longest time?
--
-- Insight:
-- Helps identify delayed deliveries.

SELECT
    order_id,
    actual_delivery_minutes,
    RANK()
    OVER(ORDER BY actual_delivery_minutes DESC) AS delivery_rank
FROM orders;