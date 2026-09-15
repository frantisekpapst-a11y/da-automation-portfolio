USE pricing_control;
GO


IF OBJECT_ID('dbo.products', 'U') IS NULL
    CREATE TABLE dbo.products
    (
        product_id INT IDENTITY PRIMARY KEY,
        product_code VARCHAR(20) NOT NULL UNIQUE,
        product_name NVARCHAR(100) NOT NULL,
        purchase_currency CHAR(3) NOT NULL,
        purchase_price DECIMAL(12, 2) NOT NULL,
        is_active BIT NOT NULL DEFAULT 1
    );
GO


IF OBJECT_ID('dbo.exchange_rates', 'U') IS NULL
    CREATE TABLE dbo.exchange_rates
    (
        exchange_rate_id INT IDENTITY PRIMARY KEY,
        rate_date DATE NOT NULL,
        currency_code CHAR(3) NOT NULL,
        amount INT NOT NULL,
        rate_czk DECIMAL(12, 6) NOT NULL,
        downloaded_at DATETIME2 NOT NULL,

        UNIQUE (rate_date, currency_code)
    );
GO


IF OBJECT_ID('dbo.pricing_control_results', 'U') IS NULL
    CREATE TABLE dbo.pricing_control_results
    (
        control_id INT IDENTITY PRIMARY KEY,
        control_date DATE NOT NULL,
        product_id INT NOT NULL,
        purchase_currency CHAR(3) NOT NULL,
        purchase_price DECIMAL(12, 2) NOT NULL,
        amount INT NOT NULL,
        rate_czk DECIMAL(12, 6) NOT NULL,
        purchase_price_czk DECIMAL(12, 2) NOT NULL,
        minimum_price_czk DECIMAL(12, 2) NOT NULL,
        maximum_price_czk DECIMAL(12, 2) NOT NULL,
        status VARCHAR(20) NOT NULL,
        processed_at DATETIME2 NOT NULL,

        CONSTRAINT FK_pricing_control_results_products
            FOREIGN KEY (product_id)
            REFERENCES dbo.products(product_id),

        CONSTRAINT UQ_pricing_control_results
            UNIQUE (control_date, product_id)
    );
GO

SELECT
    SCHEMA_NAME(schema_id) AS schema_name,
    name AS table_name
FROM sys.tables
ORDER BY schema_name, table_name;
GO