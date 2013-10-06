SELECT outdegree, count(*)
FROM
	(
		SELECT count(*)
		FROM edge
		GROUP BY src_id
	) as outdegree
GROUP BY outdegree