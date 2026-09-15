USE pricing_control;
GO

IF NOT EXISTS (
    SELECT 1
    FROM dbo.products
)
    INSERT INTO dbo.products
    (
        product_code,
        product_name,
        purchase_currency,
        purchase_price
    )
    VALUES
        ('PRD001', N'Průmyslový snímač', 'EUR', 42.50),
        ('PRD002', N'Čtečka čárových kódů', 'USD', 115.00),
        ('PRD003', N'Balicí páska', 'CZK', 84.50),
        ('PRD004', N'Pracovní LED světlo', 'GBP', 28.00),
        ('PRD005', N'Ochranné rukavice – balení', 'PLN', 52.00),
        ('PRD006', N'Digitální posuvné měřítko', 'EUR', 36.00);
GO

SELECT *
FROM dbo.products
ORDER BY product_id;