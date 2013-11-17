create or replace function count_diff() returns integer AS
$$
DECLARE
	diff_count integer := 0;
BEGIN
	select into diff_count
		count(*)
		from component, component_tmp
		where component.nid = component_tmp.nid and component.cid <> component_tmp.cid;

	return diff_count;
END;
$$
language plpgsql;