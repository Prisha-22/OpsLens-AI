/*=========================================================
BUSINESS CASE STUDIES
=========================================================*/

-----------------------------------------------------------
-- Case Study 1 : Best Performing Restaurant
-----------------------------------------------------------
-- Business Question:
-- Which restaurant generated the highest revenue?
--
-- Insight:
-- Helps identify top-performing restaurant partners.

SELECT
    r.restaurant_name,
    ROUND(SUM(o.order_value),2) AS revenue
FROM restaurants r
JOIN orders o
ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_name
ORDER BY revenue DESC
LIMIT 10;


-----------------------------------------------------------
-- Case Study 2 : Employee of the Month
-----------------------------------------------------------
-- Business Question:
-- Which rider completed the highest number of deliveries?
--
-- Insight:
-- Identifies the best-performing delivery partner.

SELECT
    rd.rider_name,
    COUNT(o.order_id) AS deliveries
FROM riders rd
JOIN orders o
ON rd.rider_id = o.rider_id
WHERE o.delivery_status='Delivered'
GROUP BY rd.rider_name
ORDER BY deliveries DESC
LIMIT 10;


-----------------------------------------------------------
-- Case Study 3 : Highest Revenue City
-----------------------------------------------------------
-- Business Question:
-- Which city generates the highest revenue?
--
-- Insight:
-- Helps identify the strongest business market.

SELECT
    c.city,
    ROUND(SUM(o.order_value),2) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.city
ORDER BY revenue DESC;


-----------------------------------------------------------
-- Case Study 4 : Weather Impact
-----------------------------------------------------------
-- Business Question:
-- Which weather condition increases delivery time the most?
--
-- Insight:
-- Helps improve operational planning.

SELECT
    weather,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders
GROUP BY weather
ORDER BY avg_delivery_time DESC;


-----------------------------------------------------------
-- Case Study 5 : Traffic Impact
-----------------------------------------------------------
-- Business Question:
-- Which traffic level causes the greatest delivery delay?
--
-- Insight:
-- Helps optimize delivery routes.

SELECT
    traffic_level,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders
GROUP BY traffic_level
ORDER BY avg_delivery_time DESC;


-----------------------------------------------------------
-- Case Study 6 : VIP Customers
-----------------------------------------------------------
-- Business Question:
-- Who are the top spending customers?
--
-- Insight:
-- Identifies customers for loyalty and reward programs.

SELECT
    c.customer_name,
    ROUND(SUM(o.order_value),2) AS total_spent
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.customer_name
ORDER BY total_spent DESC
LIMIT 10;


-----------------------------------------------------------
-- Case Study 7 : Most Popular Cuisine
-----------------------------------------------------------
-- Business Question:
-- Which cuisine receives the highest number of orders?
--
-- Insight:
-- Helps understand customer food preferences.

SELECT
    r.cuisine,
    COUNT(o.order_id) AS total_orders
FROM restaurants r
JOIN orders o
ON r.restaurant_id=o.restaurant_id
GROUP BY r.cuisine
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- Case Study 8 : Peak Business Hours
-----------------------------------------------------------
-- Business Question:
-- During which period does the platform receive the most orders?
--
-- Insight:
-- Supports workforce planning and rider allocation.

SELECT
    peak_hour,
    COUNT(*) AS total_orders
FROM orders
GROUP BY peak_hour
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- Case Study 9 : Restaurant Delay Analysis
-----------------------------------------------------------
-- Business Question:
-- Which restaurants have the highest average delivery time?
--
-- Insight:
-- Identifies restaurants contributing to delivery delays.

SELECT
    r.restaurant_name,
    ROUND(AVG(o.actual_delivery_minutes),2) AS avg_delivery_time
FROM restaurants r
JOIN orders o
ON r.restaurant_id=o.restaurant_id
GROUP BY r.restaurant_name
ORDER BY avg_delivery_time DESC
LIMIT 10;


-----------------------------------------------------------
-- Case Study 10 : Expansion Opportunity
-----------------------------------------------------------
-- Business Question:
-- Which city has the highest customer base?
--
-- Insight:
-- Helps identify potential cities for future expansion.

SELECT
    city,
    COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY customers DESC;