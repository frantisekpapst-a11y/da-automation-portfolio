SELECT COUNT(*) AS issue_count
FROM dbo.github_issues;

SELECT TOP (5)
    issue_id,
    repository_id,
    issue_number,
    title,
    state,
    user_login,
    created_at
FROM dbo.github_issues
ORDER BY issue_number DESC;

SELECT TOP (10)
    r.repository_owner,
    r.repository_name,
    i.issue_number,
    i.title,
    i.state,
    i.user_login,
    i.created_at
FROM dbo.github_issues i
JOIN dbo.repositories r
    ON i.repository_id = r.repository_id
ORDER BY i.issue_number DESC;