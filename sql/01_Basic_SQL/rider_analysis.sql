/*=========================================================
RIDER ANALYSIS
=========================================================*/

-----------------------------------------------------------
-- 1. Total Riders
-----------------------------------------------------------
-- Business Question:
-- How many delivery partners are registered on the platform?
--
-- Insight:
-- Shows the total delivery workforce available.

SELECT
    COUNT(*) AS total_riders
FROM riders;


-----------------------------------------------------------
-- 2. Riders by Vehicle Type
-----------------------------------------------------------
-- Business Question:
-- Which vehicle type is most commonly used for deliveries?
--
-- Insight:
-- Helps understand fleet composition and transportation strategy.

SELECT
    vehicle_type,
    COUNT(*) AS total_riders
FROM riders
GROUP BY vehicle_type
ORDER BY total_riders DESC;


-----------------------------------------------------------
-- 3. Riders by Shift
-----------------------------------------------------------
-- Business Question:
-- How are riders distributed across different work shifts?
--
-- Insight:
-- Helps evaluate workforce availability throughout the day.

SELECT
    shift,
    COUNT(*) AS total_riders
FROM riders
GROUP BY shift
ORDER BY total_riders DESC;


-----------------------------------------------------------
-- 4. Average Rider Rating
-----------------------------------------------------------
-- Business Question:
-- What is the average performance rating of delivery partners?
--
-- Insight:
-- Measures the overall service quality provided by riders.

SELECT
    ROUND(AVG(rider_rating),2) AS average_rider_rating
FROM riders;


-----------------------------------------------------------
-- 5. Top 10 Rated Riders
-----------------------------------------------------------
-- Business Question:
-- Which riders consistently provide the best delivery service?
--
-- Insight:
-- Identifies high-performing riders for rewards and recognition.

SELECT
    rider_name,
    rider_rating
FROM riders
ORDER BY rider_rating DESC
LIMIT 10;


-----------------------------------------------------------
-- 6. Average Experience
-----------------------------------------------------------
-- Business Question:
-- What is the average experience level of delivery partners?
--
-- Insight:
-- Helps understand the maturity and expertise of the rider workforce.

SELECT
    ROUND(AVG(experience_years),2) AS average_experience
FROM riders;


-----------------------------------------------------------
-- 7. Most Experienced Riders
-----------------------------------------------------------
-- Business Question:
-- Which riders have the highest delivery experience?
--
-- Insight:
-- Identifies experienced riders who can handle complex deliveries.

SELECT
    rider_name,
    experience_years
FROM riders
ORDER BY experience_years DESC
LIMIT 10;


-----------------------------------------------------------
-- 8. Experience by Shift
-----------------------------------------------------------
-- Business Question:
-- Which work shift has the most experienced riders?
--
-- Insight:
-- Helps allocate experienced riders during high-demand periods.

SELECT
    shift,
    ROUND(AVG(experience_years),2) AS average_experience
FROM riders
GROUP BY shift
ORDER BY average_experience DESC;