/*=========================================================
SQL VIEWS
=========================================================*/

-----------------------------------------------------------
-- 1. Customer Order Summary View
-----------------------------------------------------------
-- Business Question:
-- Can we create a reusable report showing customer orders?
--
-- Insight:
-- Simplifies customer order analysis for dashboards.

CREATE OR REPLACE VIEW customer_order_summary AS
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.membership,
    o.order_id,
    o.order_value,
    o.delivery_status
FROM customers c
INNER JOIN orders o
ON c.customer_id = o.customer_id;


-----------------------------------------------------------
-- View Output
-----------------------------------------------------------

SELECT * FROM customer_order_summary;


-----------------------------------------------------------
-- 2. Restaurant Performance View
-----------------------------------------------------------
-- Business Question:
-- Can we create a reusable restaurant performance report?
--
-- Insight:
-- Helps monitor restaurant activity and revenue.

CREATE OR REPLACE VIEW restaurant_performance AS
SELECT
    r.restaurant_id,
    r.restaurant_name,
    r.cuisine,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_value),2) AS total_revenue
FROM restaurants r
LEFT JOIN orders o
ON r.restaurant_id = o.restaurant_id
GROUP BY
r.restaurant_id,
r.restaurant_name,
r.cuisine;

SELECT * FROM restaurant_performance;


-----------------------------------------------------------
-- 3. Rider Performance View
-----------------------------------------------------------
-- Business Question:
-- How is each rider performing?
--
-- Insight:
-- Tracks workload and average delivery time.

CREATE OR REPLACE VIEW rider_performance AS
SELECT
    rd.rider_id,
    rd.rider_name,
    COUNT(o.order_id) AS total_deliveries,
    ROUND(AVG(o.actual_delivery_minutes),2) AS avg_delivery_time
FROM riders rd
LEFT JOIN orders o
ON rd.rider_id = o.rider_id
GROUP BY
rd.rider_id,
rd.rider_name;

SELECT * FROM rider_performance;


-----------------------------------------------------------
-- 4. Revenue Summary View
-----------------------------------------------------------
-- Business Question:
-- Can we summarize revenue metrics in one reusable view?
--
-- Insight:
-- Makes reporting easier for dashboards.

CREATE OR REPLACE VIEW revenue_summary AS
SELECT
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value),2) AS total_revenue,
    ROUND(AVG(order_value),2) AS average_order_value
FROM orders;

SELECT * FROM revenue_summary;


-----------------------------------------------------------
-- 5. Delivery Performance View
-----------------------------------------------------------
-- Business Question:
-- Can we monitor delivery performance using a single view?
--
-- Insight:
-- Provides a reusable dataset for operational dashboards.

CREATE OR REPLACE VIEW delivery_performance AS
SELECT
    order_id,
    actual_delivery_minutes,
    estimated_delivery_minutes,
    delivery_status,
    traffic_level,
    weather
FROM orders;

SELECT * FROM delivery_performance;