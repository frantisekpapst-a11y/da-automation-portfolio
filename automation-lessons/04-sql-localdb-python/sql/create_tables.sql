IF OBJECT_ID('dbo.repositories', 'U') IS NULL
    CREATE TABLE dbo.repositories(
        repository_id INT IDENTITY(1, 1) PRIMARY KEY,
        repository_owner NVARCHAR(100) NOT NULL,
        repository_name NVARCHAR(200) NOT NULL
    );

SELECT *
FROM dbo.repositories;

IF OBJECT_ID('dbo.github_issues', 'U') IS NULL
    CREATE TABLE dbo.github_issues
    (
        issue_id BIGINT PRIMARY KEY,
        repository_id INT NOT NULL,
        issue_number INT NOT NULL,
        title NVARCHAR(500) NOT NULL,
        state NVARCHAR(20) NOT NULL,
        user_login NVARCHAR(100) NULL,
        created_at DATETIME2 NOT NULL,
        updated_at DATETIME2 NOT NULL,
        html_url NVARCHAR(500) NOT NULL,
        downloaded_at DATETIME2 NOT NULL,

        CONSTRAINT FK_github_issues_repositories
            FOREIGN KEY (repository_id)
            REFERENCES dbo.repositories(repository_id)
    );

SELECT *
FROM dbo.github_issues;