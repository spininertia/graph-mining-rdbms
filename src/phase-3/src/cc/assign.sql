create or replace function assign() returns void as
$$
BEGIN
update component_tmp 
	set cid = ccid
	from (
		select component.nid as nnid, component.cid as ccid
		from component
		) as cmpt
	where nid = nnid;
END;
$$
language plpgsql;

