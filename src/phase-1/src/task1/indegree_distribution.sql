SELECT indegree, count(*)
FROM
	(
		SELECT count(*)
		FROM edge
		GROUP BY dst_id
	) AS indegree
GROUP BY indegree