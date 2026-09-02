/*=========================================================
JOINS
=========================================================*/

-----------------------------------------------------------
-- 1. Customer Orders
-----------------------------------------------------------
-- Business Question:
-- Which customers have placed orders and what is the value of each order?
--
-- Insight:
-- Combines customer and order data to analyze customer purchasing behavior.

SELECT
    c.customer_name,
    o.order_id,
    o.order_value,
    o.delivery_status
FROM customers c
INNER JOIN orders o
ON c.customer_id = o.customer_id;


-----------------------------------------------------------
-- 2. Restaurant Orders
-----------------------------------------------------------
-- Business Question:
-- Which restaurant handled each order?
--
-- Insight:
-- Helps analyze restaurant performance and workload.

SELECT
    r.restaurant_name,
    o.order_id,
    o.order_value,
    o.delivery_status
FROM restaurants r
INNER JOIN orders o
ON r.restaurant_id = o.restaurant_id;


-----------------------------------------------------------
-- 3. Rider Deliveries
-----------------------------------------------------------
-- Business Question:
-- Which rider delivered each order?
--
-- Insight:
-- Measures rider workload and delivery assignments.

SELECT
    rd.rider_name,
    o.order_id,
    o.actual_delivery_minutes
FROM riders rd
INNER JOIN orders o
ON rd.rider_id = o.rider_id;


-----------------------------------------------------------
-- 4. Customer + Restaurant
-----------------------------------------------------------
-- Business Question:
-- Which customer ordered from which restaurant?
--
-- Insight:
-- Helps understand customer preferences.

SELECT
    c.customer_name,
    r.restaurant_name,
    o.order_value
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id
INNER JOIN restaurants r
ON o.restaurant_id = r.restaurant_id;


-----------------------------------------------------------
-- 5. Complete Order Details
-----------------------------------------------------------
-- Business Question:
-- Show complete order information including customer,
-- restaurant and rider.

-- Insight:
-- Creates a complete operational view of every order.

SELECT
    o.order_id,
    c.customer_name,
    r.restaurant_name,
    rd.rider_name,
    o.order_value,
    o.delivery_status
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id
INNER JOIN restaurants r
ON o.restaurant_id = r.restaurant_id
INNER JOIN riders rd
ON o.rider_id = rd.rider_id;


-----------------------------------------------------------
-- 6. Payments for Orders
-----------------------------------------------------------
-- Business Question:
-- Which payment belongs to which order?
--
-- Insight:
-- Connects financial and operational data.

SELECT
    o.order_id,
    p.payment_mode,
    p.amount,
    p.payment_status
FROM orders o
INNER JOIN payments p
ON o.order_id = p.order_id;


-----------------------------------------------------------
-- 7. Customer Ratings
-----------------------------------------------------------
-- Business Question:
-- Which customer gave which rating?
--
-- Insight:
-- Helps analyze customer satisfaction.

SELECT
    c.customer_name,
    rt.customer_rating,
    rt.feedback
FROM ratings rt
INNER JOIN orders o
ON rt.order_id = o.order_id
INNER JOIN customers c
ON o.customer_id = c.customer_id;


-----------------------------------------------------------
-- 8. Restaurant Ratings
-----------------------------------------------------------
-- Business Question:
-- Which restaurants received the highest ratings?
--
-- Insight:
-- Evaluates restaurant quality.

SELECT
    r.restaurant_name,
    rt.restaurant_rating
FROM ratings rt
INNER JOIN orders o
ON rt.order_id = o.order_id
INNER JOIN restaurants r
ON o.restaurant_id = r.restaurant_id;


-----------------------------------------------------------
-- 9. Rider Ratings
-----------------------------------------------------------
-- Business Question:
-- Which riders received the highest customer ratings?
--
-- Insight:
-- Measures rider performance.

SELECT
    rd.rider_name,
    rt.rider_rating
FROM ratings rt
INNER JOIN orders o
ON rt.order_id = o.order_id
INNER JOIN riders rd
ON o.rider_id = rd.rider_id;


-----------------------------------------------------------
-- 10. Complete Business Report
-----------------------------------------------------------
-- Business Question:
-- Show all business information for every completed order.
--
-- Insight:
-- Creates a unified dataset for dashboards and business reporting.

SELECT
    o.order_id,
    c.customer_name,
    r.restaurant_name,
    rd.rider_name,
    p.payment_mode,
    o.order_value,
    rt.customer_rating,
    o.delivery_status
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id
INNER JOIN restaurants r
ON o.restaurant_id = r.restaurant_id
INNER JOIN riders rd
ON o.rider_id = rd.rider_id
INNER JOIN payments p
ON o.order_id = p.order_id
INNER JOIN ratings rt
ON o.order_id = rt.order_id;