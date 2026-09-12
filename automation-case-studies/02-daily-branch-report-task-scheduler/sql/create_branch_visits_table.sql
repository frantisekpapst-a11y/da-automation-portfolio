USE automation_practice;
GO

IF OBJECT_ID(N'dbo.branch_visits', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.branch_visits
    (
        visit_id NVARCHAR(30) NOT NULL,
        branch_code NVARCHAR(10) NOT NULL,
        visit_date DATE NOT NULL,
        customer_id INT NOT NULL,
        service_type NVARCHAR(50) NOT NULL,
        duration_minutes INT NOT NULL,
        status NVARCHAR(20) NOT NULL,
        source_file NVARCHAR(255) NOT NULL,
        loaded_at DATETIME2 NOT NULL
            CONSTRAINT DF_branch_visits_loaded_at
            DEFAULT SYSDATETIME(),

        CONSTRAINT PK_branch_visits
            PRIMARY KEY (visit_id),

        CONSTRAINT CK_branch_visits_duration
            CHECK (duration_minutes >= 0)
    );
END;
GO

SELECT TOP (10) *
FROM dbo.branch_visits;
GO

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT visit_id) AS unique_visits,
    MIN(loaded_at) AS first_loaded_at,
    MAX(loaded_at) AS last_loaded_at
FROM dbo.branch_visits;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT visit_id) AS unique_visits
FROM dbo.branch_visits;

SELECT
    branch_code,
    COUNT(*) AS visit_count,
    SUM(duration_minutes) AS total_duration_minutes
FROM dbo.branch_visits
WHERE visit_date = '2026-09-12'
GROUP BY branch_code
ORDER BY branch_code;