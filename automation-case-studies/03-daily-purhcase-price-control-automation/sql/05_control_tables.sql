USE pricing_control;

GO


-- 1. Počet kurzů za jednotlivé dny
SELECT
    rate_date,
    COUNT(*) AS rate_count,
    MIN(downloaded_at) AS downloaded_at
FROM dbo.exchange_rates
GROUP BY rate_date
ORDER BY rate_date DESC;

GO


-- 2. Počet výsledků a jejich stav za jednotlivé dny
SELECT
    control_date,
    status,
    COUNT(*) AS product_count
FROM dbo.pricing_control_results
GROUP BY
    control_date,
    status
ORDER BY
    control_date DESC,
    status;

GO


-- 3. Podrobné výsledky cenové kontroly
SELECT
    r.control_date,
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
    ON r.product_id = p.product_id
ORDER BY
    r.control_date DESC,
    p.product_code;

GO


-- 4. Kontrola duplicitních kurzů
SELECT
    rate_date,
    currency_code,
    COUNT(*) AS duplicate_count
FROM dbo.exchange_rates
GROUP BY
    rate_date,
    currency_code
HAVING COUNT(*) > 1;

GO


-- 5. Kontrola duplicitních výsledků
SELECT
    control_date,
    product_id,
    COUNT(*) AS duplicate_count
FROM dbo.pricing_control_results
GROUP BY
    control_date,
    product_id
HAVING COUNT(*) > 1;

GO