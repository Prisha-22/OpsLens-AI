/*=========================================================
DELIVERY KPIs
=========================================================*/

-----------------------------------------------------------
-- KPI 1 : Average Delivery Time
-----------------------------------------------------------
-- Business KPI:
-- What is the average time taken to complete deliveries?
--
-- Insight:
-- Measures overall delivery efficiency.

SELECT
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders;


-----------------------------------------------------------
-- KPI 2 : Average Estimated Delivery Time
-----------------------------------------------------------
-- Business KPI:
-- What is the average estimated delivery time promised to customers?
--
-- Insight:
-- Helps compare promised vs actual delivery performance.

SELECT
    ROUND(AVG(estimated_delivery_minutes),2) AS avg_estimated_delivery_time
FROM orders;


-----------------------------------------------------------
-- KPI 3 : On-Time Delivery Rate
-----------------------------------------------------------
-- Business KPI:
-- What percentage of orders are delivered on or before the estimated time?
--
-- Insight:
-- Measures service reliability and customer satisfaction.

SELECT
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS on_time_delivery_rate
FROM orders
WHERE actual_delivery_minutes <= estimated_delivery_minutes;


-----------------------------------------------------------
-- KPI 4 : Average Delivery Distance
-----------------------------------------------------------
-- Business KPI:
-- What is the average delivery distance per order?
--
-- Insight:
-- Helps optimize delivery zones and rider allocation.

SELECT
    ROUND(AVG(distance_km),2) AS avg_delivery_distance
FROM orders;


-----------------------------------------------------------
-- KPI 5 : Delivery Status Distribution
-----------------------------------------------------------
-- Business KPI:
-- What is the distribution of delivered, delayed, and cancelled orders?
--
-- Insight:
-- Measures operational performance and service quality.

SELECT
    delivery_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY delivery_status
ORDER BY total_orders DESC;


-----------------------------------------------------------
-- KPI 6 : Cancellation Rate
-----------------------------------------------------------
-- Business KPI:
-- What percentage of orders are cancelled?
--
-- Insight:
-- Helps identify operational issues and customer dissatisfaction.

SELECT
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM orders),
        2
    ) AS cancellation_rate
FROM orders
WHERE delivery_status = 'Cancelled';


-----------------------------------------------------------
-- KPI 7 : Average Delivery Time by Traffic Level
-----------------------------------------------------------
-- Business KPI:
-- How does traffic impact delivery time?
--
-- Insight:
-- Supports route planning and rider scheduling.

SELECT
    traffic_level,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders
GROUP BY traffic_level
ORDER BY avg_delivery_time DESC;


-----------------------------------------------------------
-- KPI 8 : Average Delivery Time by Weather
-----------------------------------------------------------
-- Business KPI:
-- How does weather affect delivery time?
--
-- Insight:
-- Helps prepare for operational challenges during different weather conditions.

SELECT
    weather,
    ROUND(AVG(actual_delivery_minutes),2) AS avg_delivery_time
FROM orders
GROUP BY weather
ORDER BY avg_delivery_time DESC;