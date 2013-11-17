--hop.sql
select hops.id, min(hops.hop) from hops, (select id, max(size) as max_size from hops group by id) as foo
where hops.id = foo.id and hops.size = foo.max_size
group by hops.id;