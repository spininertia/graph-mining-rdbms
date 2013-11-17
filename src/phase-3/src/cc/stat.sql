create or replace function cc_stat() returns void as
$$
DECLARE
num_cc integer := 0;
max_node integer := 0;
BEGIN
select into num_cc count(distinct cid) from component;
RAISE NOTICE 'number of connected components: %', num_cc;
select into max_node count(*) from component group by cid order by count(*) desc limit 1;
RAISE NOTICE 'number of nodes in max WSC: %', max_node;
END;
$$
language plpgsql;