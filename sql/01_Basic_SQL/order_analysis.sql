/*=========================================================
ORDER ANALYSIS
=========================================================*/

-----------------------------------------------------------
-- 1. Total Orders
-----------------------------------------------------------
-- Business Question:
-- How many orders have been placed on the platform?
--
-- Insight:
-- Shows the total number of orders processed and helps
-- measure overall business demand.

SELECT
    COUNT(*) AS total_orders
FROM orders;


-----------------------------------------------------------
-- 2. Orders by Delivery Status
-----------------------------------------------------------
-- Business Question:
-- What is the distribution of delivered, cancelled,
-- and delayed orders?
--
-- Insight:
-- Helps evaluate operational efficiency and identify
-- potential service issues.

SELECT
    delivery_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY delivery_status
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- 3. Total Revenue
-----------------------------------------------------------
-- Business Question:
-- How much revenue has been generated from all orders?
--
-- Insight:
-- Measures the overall financial performance of the
-- delivery platform.

SELECT
    ROUND(SUM(order_value), 2) AS total_revenue
FROM orders;


-----------------------------------------------------------
-- 4. Average Order Value
-----------------------------------------------------------
-- Business Question:
-- How much does an average customer spend per order?
--
-- Insight:
-- Helps understand customer spending behavior and
-- supports pricing and promotional strategies.

SELECT
    ROUND(AVG(order_value), 2) AS average_order_value
FROM orders;


-----------------------------------------------------------
-- 5. Average Delivery Time
-----------------------------------------------------------
-- Business Question:
-- What is the average delivery time for completed orders?
--
-- Insight:
-- Measures delivery performance and customer service efficiency.

SELECT
    ROUND(AVG(actual_delivery_minutes), 2) AS avg_delivery_time
FROM orders;


-----------------------------------------------------------
-- 6. Average Delivery Distance
-----------------------------------------------------------
-- Business Question:
-- What is the average delivery distance per order?
--
-- Insight:
-- Helps optimize delivery zones, rider allocation,
-- and transportation costs.

SELECT
    ROUND(AVG(distance_km), 2) AS avg_delivery_distance
FROM orders;


-----------------------------------------------------------
-- 7. Orders by Weather Condition
-----------------------------------------------------------
-- Business Question:
-- How are orders distributed across different weather conditions?
--
-- Insight:
-- Helps understand the impact of weather on customer demand
-- and delivery operations.

SELECT
    weather,
    COUNT(*) AS total_orders
FROM orders
GROUP BY weather
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- 8. Orders by Traffic Level
-----------------------------------------------------------
-- Business Question:
-- How does traffic level affect order volume?
--
-- Insight:
-- Supports route planning and helps identify periods
-- of high operational difficulty.

SELECT
    traffic_level,
    COUNT(*) AS total_orders
FROM orders
GROUP BY traffic_level
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- 9. Peak Hour Orders
-----------------------------------------------------------
-- Business Question:
-- How many orders are placed during peak and non-peak hours?
--
-- Insight:
-- Helps optimize rider scheduling and resource allocation.

SELECT
    peak_hour,
    COUNT(*) AS total_orders
FROM orders
GROUP BY peak_hour;


-----------------------------------------------------------
-- 10. Weekend vs Weekday Orders
-----------------------------------------------------------
-- Business Question:
-- How does order demand differ between weekends and weekdays?
--
-- Insight:
-- Helps forecast demand and improve workforce planning.

SELECT
    weekend,
    COUNT(*) AS total_orders
FROM orders
GROUP BY weekend;


-----------------------------------------------------------
-- 11. Order Type Distribution
-----------------------------------------------------------
-- Business Question:
-- Which order type is most frequently used by customers?
--
-- Insight:
-- Identifies customer preferences and supports service
-- improvement strategies.

SELECT
    order_type,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_type
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- 12. Top 10 Highest Value Orders
-----------------------------------------------------------
-- Business Question:
-- Which orders generated the highest revenue?
--
-- Insight:
-- Identifies high-value transactions and helps understand
-- premium customer purchasing behavior.

SELECT
    order_id,
    customer_id,
    restaurant_id,
    order_value
FROM orders
ORDER BY order_value DESC
LIMIT 10;