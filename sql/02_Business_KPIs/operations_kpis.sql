/*=========================================================
OPERATIONS KPIs
=========================================================*/

-----------------------------------------------------------
-- KPI 1 : Total Orders
-----------------------------------------------------------
-- Business KPI:
-- How many orders have been processed?
--
-- Insight:
-- Measures the overall workload handled by the platform.

SELECT
    COUNT(*) AS total_orders
FROM orders;


-----------------------------------------------------------
-- KPI 2 : Delivered Orders
-----------------------------------------------------------
-- Business KPI:
-- How many orders were successfully delivered?
--
-- Insight:
-- Indicates successful operational execution.

SELECT
    COUNT(*) AS delivered_orders
FROM orders
WHERE delivery_status = 'Delivered';


-----------------------------------------------------------
-- KPI 3 : Delivery Success Rate
-----------------------------------------------------------
-- Business KPI:
-- What percentage of orders are successfully delivered?
--
-- Insight:
-- Measures overall operational efficiency.

SELECT
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS delivery_success_rate
FROM orders
WHERE delivery_status = 'Delivered';


-----------------------------------------------------------
-- KPI 4 : Delayed Orders
-----------------------------------------------------------
-- Business KPI:
-- How many orders were delayed?
--
-- Insight:
-- Helps monitor delivery performance.

SELECT
    COUNT(*) AS delayed_orders
FROM orders
WHERE delivery_status = 'Delayed';


-----------------------------------------------------------
-- KPI 5 : Delayed Order Rate
-----------------------------------------------------------
-- Business KPI:
-- What percentage of orders are delayed?
--
-- Insight:
-- Identifies service quality issues.

SELECT
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS delayed_order_rate
FROM orders
WHERE delivery_status = 'Delayed';


-----------------------------------------------------------
-- KPI 6 : Cancelled Orders
-----------------------------------------------------------
-- Business KPI:
-- How many orders were cancelled?
--
-- Insight:
-- Measures order cancellation volume.

SELECT
    COUNT(*) AS cancelled_orders
FROM orders
WHERE delivery_status = 'Cancelled';


-----------------------------------------------------------
-- KPI 7 : Average Preparation vs Delivery Time
-----------------------------------------------------------
-- Business KPI:
-- How does estimated delivery time compare with actual delivery time?
--
-- Insight:
-- Helps identify operational delays.

SELECT
    ROUND(AVG(estimated_delivery_minutes),2) AS avg_estimated_time,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_actual_time
FROM orders;


-----------------------------------------------------------
-- KPI 8 : Peak Hour Demand
-----------------------------------------------------------
-- Business KPI:
-- How many orders are placed during peak hours?
--
-- Insight:
-- Helps optimize rider scheduling and resource allocation.

SELECT
    peak_hour,
    COUNT(*) AS total_orders
FROM orders
GROUP BY peak_hour
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- KPI 9 : Traffic Impact
-----------------------------------------------------------
-- Business KPI:
-- Which traffic level results in the highest delivery time?
--
-- Insight:
-- Supports route optimization and operational planning.

SELECT
    traffic_level,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders
GROUP BY traffic_level
ORDER BY avg_delivery_time DESC;


-----------------------------------------------------------
-- KPI 10 : Weather Impact
-----------------------------------------------------------
-- Business KPI:
-- Which weather condition has the highest average delivery time?
--
-- Insight:
-- Helps prepare operations during adverse weather.

SELECT
    weather,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders
GROUP BY weather
ORDER BY avg_delivery_time DESC;