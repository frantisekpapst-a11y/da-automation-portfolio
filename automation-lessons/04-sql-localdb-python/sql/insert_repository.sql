IF NOT EXISTS
(
    SELECT 1
    FROM dbo.repositories
    WHERE repository_owner = 'pandas-dev'
      AND repository_name = 'pandas'
)
    INSERT INTO dbo.repositories
    (
        repository_owner,
        repository_name
    )
    VALUES
    (
        'pandas-dev',
        'pandas'
    );

SELECT *
FROM dbo.repositories;