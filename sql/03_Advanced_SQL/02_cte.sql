/*=========================================================
COMMON TABLE EXPRESSIONS (CTE)
=========================================================*/

-----------------------------------------------------------
-- 1. Customers with Above Average Orders
-----------------------------------------------------------
-- Business Question:
-- Which customers have placed more orders than the average customer?
--
-- Insight:
-- Identifies highly active customers.

WITH avg_orders AS
(
    SELECT AVG(total_orders) AS average_orders
    FROM customers
)

SELECT
    customer_name,
    total_orders
FROM customers, avg_orders
WHERE total_orders > average_orders;


-----------------------------------------------------------
-- 2. High Value Orders
-----------------------------------------------------------
-- Business Question:
-- Which orders have a value higher than the average order value?
--
-- Insight:
-- Identifies premium transactions.

WITH avg_order_value AS
(
    SELECT AVG(order_value) AS avg_value
    FROM orders
)

SELECT
    order_id,
    order_value
FROM orders, avg_order_value
WHERE order_value > avg_value;


-----------------------------------------------------------
-- 3. Restaurants Above Average Rating
-----------------------------------------------------------
-- Business Question:
-- Which restaurants have ratings above the platform average?
--
-- Insight:
-- Identifies top-performing restaurants.

WITH avg_rating AS
(
    SELECT AVG(rating) AS average_rating
    FROM restaurants
)

SELECT
    restaurant_name,
    rating
FROM restaurants, avg_rating
WHERE rating > average_rating;


-----------------------------------------------------------
-- 4. Experienced Riders
-----------------------------------------------------------
-- Business Question:
-- Which riders have more experience than the average rider?
--
-- Insight:
-- Identifies experienced delivery partners.

WITH avg_experience AS
(
    SELECT AVG(experience_years) AS average_experience
    FROM riders
)

SELECT
    rider_name,
    experience_years
FROM riders, avg_experience
WHERE experience_years > average_experience;


-----------------------------------------------------------
-- 5. Cities with Above Average Customers
-----------------------------------------------------------
-- Business Question:
-- Which cities have more customers than the average city?
--
-- Insight:
-- Identifies strong customer markets.

WITH city_customers AS
(
    SELECT
        city,
        COUNT(*) AS total_customers
    FROM customers
    GROUP BY city
),
average_city AS
(
    SELECT AVG(total_customers) AS avg_customers
    FROM city_customers
)

SELECT
    city,
    total_customers
FROM city_customers, average_city
WHERE total_customers > avg_customers;


-----------------------------------------------------------
-- 6. Delivery Time Analysis
-----------------------------------------------------------
-- Business Question:
-- Which deliveries took longer than the average delivery time?
--
-- Insight:
-- Helps identify delayed deliveries.

WITH avg_delivery AS
(
    SELECT AVG(actual_delivery_minutes) AS avg_time
    FROM orders
)

SELECT
    order_id,
    actual_delivery_minutes
FROM orders, avg_delivery
WHERE actual_delivery_minutes > avg_time;


-----------------------------------------------------------
-- 7. High Revenue Restaurants
-----------------------------------------------------------
-- Business Question:
-- Which restaurants generated above-average revenue?
--
-- Insight:
-- Identifies the highest-performing restaurants.

WITH restaurant_revenue AS
(
    SELECT
        restaurant_id,
        SUM(order_value) AS revenue
    FROM orders
    GROUP BY restaurant_id
),
avg_revenue AS
(
    SELECT AVG(revenue) AS avg_rev
    FROM restaurant_revenue
)

SELECT
    r.restaurant_name,
    rr.revenue
FROM restaurant_revenue rr
INNER JOIN restaurants r
ON rr.restaurant_id = r.restaurant_id
CROSS JOIN avg_revenue
WHERE rr.revenue > avg_rev;


-----------------------------------------------------------
-- 8. Premium Customers
-----------------------------------------------------------
-- Business Question:
-- Which Premium members have placed more than 20 orders?
--
-- Insight:
-- Identifies highly valuable Premium customers.

WITH premium_customers AS
(
    SELECT
        customer_name,
        total_orders
    FROM customers
    WHERE membership = 'Premium'
)

SELECT *
FROM premium_customers
WHERE total_orders > 20;