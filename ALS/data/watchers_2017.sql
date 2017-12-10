SELECT w.repo_id,w.user_id,w.created_at
FROM [ghtorrent-bq:ght_2017_09_01.watchers] as w
JOIN [ghtorrent-bq:ght_2017_09_01.projects] as p ON p.id=w.repo_id
WHERE YEAR(p.created_at)=2017
