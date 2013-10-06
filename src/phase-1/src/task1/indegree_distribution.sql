SELECT indegree, count(*)
FROM
	(
		SELECT count(*)
		FROM graph
		GROUP BY to_node
	) AS indegree
GROUP BY indegree