# OpsLens AI

## Dataset Design Document

Version 1.0

Author:
Prisha Shah

Project:
Delivery Operations Intelligence Platform

## Introduction

The OpsLens AI platform is designed to analyse delivery operations data for logistics and food delivery companies. The project focuses on identifying operational bottlenecks, monitoring key performance indicators (KPIs), and generating insights to improve delivery efficiency.

To achieve this, the system requires a well-structured relational database that stores information about customers, restaurants, riders, orders, payments, and ratings. Each table represents a real-world business entity and is connected through relationships to support meaningful analysis.


# Customers Table

### Purpose
The Customers table stores information about every customer who places orders using the delivery platform. It helps analyse customer behaviour, order frequency, customer retention, and geographical distribution.

### Columns
| Column Name | Data Type | Description |
|--------------|----------|-------------|
| Customer_ID | VARCHAR | Unique customer identifier |
| Customer_Name | VARCHAR | Customer name |
| City | VARCHAR | Customer city |
| Zone | VARCHAR | Customer area or locality |
| Signup_Date | DATE | Date of registration |
| Membership | VARCHAR | Membership type (Normal, Gold, Premium) |
| Total_Orders | INTEGER | Total orders placed |


# Restaurants Table

### Purpose
The Restaurants table stores details of partner restaurants. It allows analysis of restaurant performance, preparation time, customer ratings, and order volume.

### Columns
| Column Name | Data Type | Description |
|--------------|----------|-------------|
| Restaurant_ID | VARCHAR | Unique restaurant identifier |
| Restaurant_Name | VARCHAR | Restaurant name |
| Cuisine | VARCHAR | Cuisine served |
| City | VARCHAR | Restaurant city |
| Zone | VARCHAR | Restaurant locality |
| Average_Preparation_Time | INTEGER | Average preparation time in minutes |
| Rating | DECIMAL | Restaurant rating |


# Riders Table

### Purpose
The Riders table stores information about delivery partners responsible for delivering customer orders.

### Columns
| Column Name | Data Type | Description |
|--------------|----------|-------------|
| Rider_ID | VARCHAR | Unique rider identifier |
| Rider_Name | VARCHAR | Rider name |
| Vehicle_Type | VARCHAR | Bike, Cycle, Scooter |
| Experience_Years | INTEGER | Years of experience |
| Shift | VARCHAR | Morning, Afternoon or Night |
| Rider_Rating | DECIMAL | Average rider rating |


# Orders Table

### Purpose
The Orders table acts as the central table of the database. Every delivery transaction is recorded here and linked to customers, restaurants, riders, payments, and ratings.

### Columns
| Column Name | Data Type | Description |
|--------------|----------|-------------|
| Order_ID | VARCHAR | Unique order identifier |
| Customer_ID | VARCHAR | Customer placing the order |
| Restaurant_ID | VARCHAR | Restaurant fulfilling the order |
| Rider_ID | VARCHAR | Assigned rider |
| Order_Time | DATETIME | Order placed time |
| Pickup_Time | DATETIME | Rider pickup time |
| Delivery_Time | DATETIME | Delivery completion time |
| Distance_km | DECIMAL | Delivery distance |
| Weather | VARCHAR | Weather condition |
| Traffic | VARCHAR | Traffic level |
| Order_Value | DECIMAL | Total order value |
| Delivery_Status | VARCHAR | Delivered, Cancelled, Delayed |


# Ratings Table

### Purpose
Stores customer feedback for completed orders. This table helps evaluate service quality and customer satisfaction.

### Columns
| Column Name | Data Type | Description |
|--------------|----------|-------------|
| Rating_ID | VARCHAR | Unique rating identifier |
| Order_ID | VARCHAR | Associated order |
| Customer_Rating | INTEGER | Rating given by customer |
| Rider_Rating | INTEGER | Rating for rider |
| Restaurant_Rating | INTEGER | Rating for restaurant |
| Feedback | TEXT | Customer comments |


# Payments Table

### Purpose
Stores payment information for every order placed on the platform.

### Columns
| Column Name | Data Type | Description |
|--------------|----------|-------------|
| Payment_ID | VARCHAR | Unique payment identifier |
| Order_ID | VARCHAR | Associated order |
| Payment_Mode | VARCHAR | UPI, Card, Cash |
| Amount | DECIMAL | Order amount |
| Payment_Status | VARCHAR | Success, Failed, Refunded |


## Summary

The database consists of six interconnected tables designed to simulate a real-world food delivery platform. The Orders table serves as the central entity, linking customers, restaurants, riders, payments, and ratings. This relational design enables comprehensive business analysis while reducing data redundancy and supporting efficient querying.
