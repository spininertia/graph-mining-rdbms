-- component id is the minimum node id of all nodes in the component
-- component table(nid, cid)
-- since we are computing weakly connecte components
CREATE or REPLACE FUNCTION update_component() returns void AS
$$
BEGIN
update component
	set cid = new_cid
	from (
		select dst_id as id, min(component.cid) as new_cid
		from edge, component
		where src_id = component.nid 
		group by id
		) as newComponent
	where nid = id and new_cid < cid;

update component
	set cid = new_cid
	from (
		select src_id as id, min(component.cid) as new_cid
		from edge, component
		where dst_id = component.nid 
		group by id
		) as newComponent
	where nid = id and new_cid < cid;
END;
$$
language plpgsql;
