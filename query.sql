WITH base as
(
	select 
	id.itemID as parent_itemID
	, idv.value as title
	, A.itemID
	, A.path
	, B.key
	, REPLACE(
		(SELECT file FROM pragma_database_list WHERE name = 'main')
		, 'zotero.sqlite'
		, 'storage/'||B.key
		) as partial_path
	, REPLACE(
		(SELECT file FROM pragma_database_list WHERE name = 'main')
		, 'zotero.sqlite'
		, REPLACE(A.PATH,'storage:','storage/'||B.key||'/') 
		) as full_path
	, C.tags_list
	, B.dateAdded
	, B.dateModified
	, B.clientDateModified
	from itemData id 
	left join itemDataValues idv on id.valueID = idv.valueID 
	left join (
		SELECT * 
		FROM itemAttachments ia
		where 1 = 1
		and contentType = 'application/pdf'
	) A on id.itemID = A.parentItemID
	left join items B on A.itemID = B.itemID 
	left join (	
		select 
			AA.itemID
			, GROUP_CONCAT(BB.name, ', ') AS tags_list
			from itemTags AA
			left join tags BB on AA.tagID = BB.tagID 
			group by AA.itemID
	) C on id.itemID = C.itemID
	where 1=1
	and fieldID = 1 -- title
	AND id.itemID in
	(
		select itemID 
		from collectionItems ci
		where collectionID = 8
	)
	AND A.itemID is not NULL
)
SELECT 
clientDateModified
, title
, tags_list
, partial_path
, full_path
from base
where 1=1
AND title like '%Reinforcement%'
AND tags_list like '%next%'
order by clientDateModified desc