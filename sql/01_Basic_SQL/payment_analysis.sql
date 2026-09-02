/*=========================================================
PAYMENT ANALYSIS
=========================================================*/

-----------------------------------------------------------
-- 1. Total Payments
-----------------------------------------------------------
-- Business Question:
-- How many payments have been processed?
--
-- Insight:
-- Shows the total number of payment transactions.

SELECT
    COUNT(*) AS total_payments
FROM payments;


-----------------------------------------------------------
-- 2. Payments by Payment Mode
-----------------------------------------------------------
-- Business Question:
-- Which payment method is most preferred by customers?
--
-- Insight:
-- Helps understand customer payment preferences.

SELECT
    payment_mode,
    COUNT(*) AS total_payments
FROM payments
GROUP BY payment_mode
ORDER BY total_payments DESC;


-----------------------------------------------------------
-- 3. Payments by Status
-----------------------------------------------------------
-- Business Question:
-- How many payments were successful, failed, or refunded?
--
-- Insight:
-- Measures payment system reliability.

SELECT
    payment_status,
    COUNT(*) AS total_payments
FROM payments
GROUP BY payment_status
ORDER BY total_payments DESC;


-----------------------------------------------------------
-- 4. Total Payment Amount
-----------------------------------------------------------
-- Business Question:
-- What is the total payment amount processed?
--
-- Insight:
-- Indicates the total financial transactions handled by the platform.

SELECT
    ROUND(SUM(amount),2) AS total_amount
FROM payments;


-----------------------------------------------------------
-- 5. Average Payment Amount
-----------------------------------------------------------
-- Business Question:
-- What is the average payment amount per transaction?
--
-- Insight:
-- Helps understand average customer spending.

SELECT
    ROUND(AVG(amount),2) AS average_payment
FROM payments;


-----------------------------------------------------------
-- 6. Payment Amount by Payment Mode
-----------------------------------------------------------
-- Business Question:
-- Which payment method contributes the highest transaction value?
--
-- Insight:
-- Identifies the payment channels generating the most revenue.

SELECT
    payment_mode,
    ROUND(SUM(amount),2) AS total_amount
FROM payments
GROUP BY payment_mode
ORDER BY total_amount DESC;


-----------------------------------------------------------
-- 7. Failed Payments
-----------------------------------------------------------
-- Business Question:
-- How many payment failures occurred?
--
-- Insight:
-- Helps identify payment gateway or transaction issues.

SELECT
    COUNT(*) AS failed_payments
FROM payments
WHERE payment_status = 'Failed';


-----------------------------------------------------------
-- 8. Refunded Payments
-----------------------------------------------------------
-- Business Question:
-- How many payments were refunded?
--
-- Insight:
-- Helps monitor refund trends and customer satisfaction.

SELECT
    COUNT(*) AS refunded_payments
FROM payments
WHERE payment_status = 'Refunded';