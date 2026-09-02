# OpsLens AI

# Database Architecture

## Introduction

The OpsLens AI database follows a relational database design. Instead of storing all information in one large table, the system separates data into multiple related tables. Each table represents a different business entity, such as customers, restaurants, riders, orders, payments, and ratings.

This approach reduces duplicate data, improves data consistency, and makes querying faster and easier.


# Primary Key

A Primary Key is a column that uniquely identifies every record in a table.

Examples:

Customer_ID

Restaurant_ID

Order_ID

Rider_ID

Payment_ID

Rating_ID

Every table should have one Primary Key.


# Foreign Key

A Foreign Key is a column that connects one table with another table.

For example,

Customer_ID inside the Orders table refers to the Customer_ID in the Customers table.

This creates a relationship between the two tables.


# Table Relationships
| Parent Table | Child Table | Relationship                           |
| ------------ | ----------- | -------------------------------------- |
| Customers    | Orders      | One customer can place many orders     |
| Restaurants  | Orders      | One restaurant can receive many orders |
| Riders       | Orders      | One rider can deliver many orders      |
| Orders       | Payments    | One order has one payment              |
| Orders       | Ratings     | One order has one rating               |
