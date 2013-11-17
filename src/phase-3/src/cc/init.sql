create or replace function init_component() returns void AS
$$
BEGIN
drop table if exists component;
drop table if exists component_tmp;
drop index if exists c_index;
drop index if exists ct_index;
create table component (nid int not null unique, cid int);
create table component_tmp (nid int, cid int);
insert into component_tmp(nid, cid) select distinct src_id, src_id from edge;
insert into component_tmp(nid, cid)	select distinct dst_id, dst_id from edge;
insert into component (nid, cid) select distinct nid, cid from component_tmp;
drop table component_tmp;
create table component_tmp (nid int, cid int);
insert into component_tmp (nid, cid) select nid, cid from component;
create index c_index on component (nid);
create index ct_index on component_tmp (nid);
RAISE NOTICE 'component table initialization complete.';
END;
$$
language plpgsql;