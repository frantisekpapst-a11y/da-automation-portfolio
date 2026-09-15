IF DB_ID('pricing_control') IS NULL
    CREATE DATABASE pricing_control;
GO

USE pricing_control;
GO

SELECT DB_NAME() AS current_database;