SELECT id, owner_id,name,language,created_at, forked_from, deleted, forked_from_commit_id
FROM [ghtorrent-bq:ght_2017_09_01.projects] 
WHERE YEAR(created_at)=2017 AND forked_from IS NULL
