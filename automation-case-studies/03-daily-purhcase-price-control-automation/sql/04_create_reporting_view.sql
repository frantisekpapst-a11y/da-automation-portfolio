USE pricing_control;

GO


CREATE OR ALTER VIEW dbo.vw_pricing_control_report
AS

SELECT
    r.control_date,
    r.product_id,
    p.product_code,
    p.product_name,
    r.purchase_currency,
    r.purchase_price,
    r.amount,
    r.rate_czk,
    r.purchase_price_czk,
    r.minimum_price_czk,
    r.maximum_price_czk,
    r.status,
    r.processed_at

FROM dbo.pricing_control_results r

JOIN dbo.products p
    ON r.product_id = p.product_id;

GO


SELECT *
FROM dbo.vw_pricing_control_report
ORDER BY
    control_date DESC,
    product_code;

GO