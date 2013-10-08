CREATE OR REPLACE FUNCTION calc_pagerank() RETURNS VOID AS
$$
DECLARE
    currentIndex integer;
    diff real;
    num_of_nodes integer;
    damper real;
    nrank real;
    src_degree integer;
    nid integer;
    sid integer;
BEGIN
    drop table if exists pagerank;
    drop table if exists pagerank_tmp;
    drop table if exists out_degree;
    drop table if exists trans;

    -- init pagerank
    -- first insert all nodes into a tmp table allow duplicate, then clean up
    create table pagerank_tmp(node_id int, rank real);
    create table pagerank(node_id int primary key, rank real);    
    insert into pagerank_tmp(node_id, rank) select src_id, 1.0 from edge;
    insert into pagerank_tmp(node_id, rank) select dst_id, 1.0 from edge;
    select count(*) into num_of_nodes from pagerank_tmp group by node_id;
    insert into pagerank(node_id, rank) select node_id, 1.0/num_of_nodes from pagerank_tmp group by node_id;
    delete from pagerank_tmp;
    insert into pagerank_tmp(node_id, rank) select node_id,rank from pagerank;

    -- init out degree
    create table out_degree(node_id int primary key, degree int);
    insert into out_degree(node_id, degree) select src_id, count(*) from edge group by src_id;

    -- init transfer weight matrix
    create table trans(dst_id int, src_id int, weight real);
    insert into trans select dst_id, src_id, 1.0/OD.degree from edge, out_degree as OD where edge.src_id = OD.node_id;

    currentIndex := 0;
    damper := 0.85;
    while currentIndex < 100 loop
        RAISE NOTICE 'currentIndex: %', currentIndex;

        for nid, nrank in 
        select trans.dst_id, (1 - damper)/num_of_nodes + damper * sum(trans.weight * pagerank.rank) 
        from trans, pagerank where trans.src_id = pagerank.node_id 
        group by trans.dst_id loop
            -- update tmperorary pagerank
            update pagerank_tmp set rank = nrank where node_id = nid;        
        end loop;

        select sum( (N.rank - O.rank) * (N.rank - O.rank) ) into diff 
        from pagerank as O, pagerank_tmp as N where O.node_id = N.node_id;

        RAISE NOTICE 'diff: %', diff;
        delete from pagerank;
        insert into pagerank select * from pagerank_tmp;

        currentIndex := currentIndex + 1;
        if diff < 0.0001 then
            exit;
        end if;
    end loop;
    drop table pagerank_tmp;

    RAISE NOTICE 'pagerank done. check the table pagerank.';
END;
$$
LANGUAGE plpgsql;