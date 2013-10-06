SELECT outdegree, count(*)
FROM
	(
		SELECT count(*)
		FROM graph
		GROUP BY from_node
	) as outdegree
GROUP BY outdegree