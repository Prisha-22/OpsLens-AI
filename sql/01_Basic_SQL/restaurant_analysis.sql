/*=========================================================
RESTAURANT ANALYSIS
=========================================================*/

-----------------------------------------------------------
-- 1. Total Restaurants
-----------------------------------------------------------
-- Business Question:
-- How many restaurants are partnered with the platform?
--
-- Insight:
-- Shows the total number of active restaurant partners.

SELECT
    COUNT(*) AS total_restaurants
FROM restaurants;


-----------------------------------------------------------
-- 2. Restaurants by Cuisine
-----------------------------------------------------------
-- Business Question:
-- Which cuisine category has the highest number of restaurants?
--
-- Insight:
-- Helps understand cuisine distribution and customer choices.

SELECT
    cuisine,
    COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY cuisine
ORDER BY total_restaurants DESC;


-----------------------------------------------------------
-- 3. Restaurants by City
-----------------------------------------------------------
-- Business Question:
-- Which cities have the highest number of restaurant partners?
--
-- Insight:
-- Identifies cities with strong restaurant coverage.

SELECT
    city,
    COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY city
ORDER BY total_restaurants DESC;


-----------------------------------------------------------
-- 4. Average Restaurant Rating
-----------------------------------------------------------
-- Business Question:
-- What is the average rating of restaurants on the platform?
--
-- Insight:
-- Measures the overall quality of restaurant services.

SELECT
    ROUND(AVG(rating),2) AS average_rating
FROM restaurants;


-----------------------------------------------------------
-- 5. Top 10 Rated Restaurants
-----------------------------------------------------------
-- Business Question:
-- Which restaurants have the highest customer ratings?
--
-- Insight:
-- Identifies top-performing restaurants for promotions and recommendations.

SELECT
    restaurant_name,
    rating
FROM restaurants
ORDER BY rating DESC
LIMIT 10;


-----------------------------------------------------------
-- 6. Average Preparation Time
-----------------------------------------------------------
-- Business Question:
-- What is the average food preparation time across restaurants?
--
-- Insight:
-- Helps evaluate restaurant efficiency and operational performance.

SELECT
    ROUND(AVG(average_preparation_time),2) AS average_preparation_time
FROM restaurants;


-----------------------------------------------------------
-- 7. Slowest Restaurants
-----------------------------------------------------------
-- Business Question:
-- Which restaurants take the longest time to prepare orders?
--
-- Insight:
-- Identifies restaurants that may contribute to delivery delays.

SELECT
    restaurant_name,
    average_preparation_time
FROM restaurants
ORDER BY average_preparation_time DESC
LIMIT 10;


-----------------------------------------------------------
-- 8. Restaurants by Zone
-----------------------------------------------------------
-- Business Question:
-- Which delivery zones have the highest number of restaurants?
--
-- Insight:
-- Helps identify areas with high restaurant density and potential expansion opportunities.

SELECT
    zone,
    COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY zone
ORDER BY total_restaurants DESC;