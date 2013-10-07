CREATE OR REPLACE FUNCTION pagerank() RETURNS VOID AS
$$
DECLARE
    currentIndex integer;
    diff real;
    num_of_nodes integer;
    damper real;
    new_rank real;
    old_rank real;
    src_rank real;
    src_degree integer;
    nid integer;
    sid integer;
BEGIN
    drop table if exists pagerank;
    drop table if exists pagerank_tmp;
    drop table if exists out_degree;

    -- init pagerank
    -- first insert all nodes into a tmp table allow duplicate, then clean up
    create table pagerank_tmp(node_id int, rank real);
    create table pagerank(node_id int primary key, rank real);    
    insert into pagerank_tmp(node_id, rank) select src_id, 1.0 from edge;
    insert into pagerank_tmp(node_id, rank) select dst_id, 1.0 from edge;
    insert into pagerank(node_id, rank) select node_id, 1.0 from pagerank_tmp group by node_id;
    delete from pagerank_tmp;
    insert into pagerank_tmp(node_id, rank) select node_id,rank from pagerank;

    -- init out degree
    create table out_degree(node_id int primary key, degree int);
    insert into out_degree(node_id, degree) select src_id, count(*) from edge group by src_id;

    currentIndex := 0;
    select count(*) into num_of_nodes from pagerank;
    damper := 0.8;
    while currentIndex < 20 loop
        RAISE NOTICE 'currentIndex: %', currentIndex;
        for nid in (select node_id from pagerank) loop
            select rank into old_rank from pagerank where node_id = nid;
            new_rank := (1 - damper) * old_rank / num_of_nodes;
            for sid in (select * from edge where dst_id = nid) loop
                select rank into src_rank from pagerank where node_id = sid;
                select degree into src_degree from out_degree where node_id = sid;
                new_rank := new_rank + damper * src_rank / src_degree;
            end loop;
            update pagerank_tmp set rank = new_rank where node_id = nid;
        end loop;

        select sum( (N.rank - O.rank) * (N.rank - O.rank) ) into diff from pagerank as O, pagerank_tmp as N where O.node_id = N.node_id;
        delete from pagerank;
        insert into pagerank select * from pagerank_tmp;
        currentIndex := currentIndex + 1;
        if diff < 0.001 then
            exit;
        end if;
    end loop;
    drop table pagerank_tmp;
    RAISE NOTICE 'pagerank done. check the table pagerank.';
END;
$$
LANGUAGE plpgsql;