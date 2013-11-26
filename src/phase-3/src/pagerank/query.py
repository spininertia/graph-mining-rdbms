rank_function = '''
CREATE OR REPLACE FUNCTION calc_pagerank() RETURNS VOID AS
$$
DECLARE
    currentIndex integer;
    diff real;
    num_of_nodes integer; 
    damper real;
    nrank real;
    nid integer;
BEGIN
    RAISE NOTICE 'Entering....';
    drop table if exists %s;
    drop table if exists pagerank_tmp;
    drop table if exists out_degree;
    drop table if exists trans;

    -- first insert all nodes into a tmp table allow duplicate, then clean up
    create table pagerank_tmp(node_id int, rank real);
    create table %s(node_id int primary key, rank real);    
    insert into pagerank_tmp(node_id, rank) select from_id, 1.0 from %s;
    insert into pagerank_tmp(node_id, rank) select to_id, 1.0 from %s;
    select count(*) into num_of_nodes from pagerank_tmp group by node_id;
    insert into %s(node_id, rank) select node_id, 1.0/num_of_nodes from pagerank_tmp group by node_id;
    delete from pagerank_tmp;
    insert into pagerank_tmp(node_id, rank) select node_id,rank from %s;

    -- init out degree
    create table out_degree(node_id int primary key, degree int);
    insert into out_degree(node_id, degree) select from_id, count(*) from %s group by from_id;

    -- init transfer weight matrix
    create table trans(to_id int, from_id int, weight real);
    insert into trans select to_id, from_id, 1.0/OD.degree from %s, out_degree as OD where %s.from_id = OD.node_id;

    currentIndex := 0;
    damper := 0.85;
    create index to_index on trans(to_id);
    create index from_index on trans(from_id);
    create index prtmp_index on pagerank_tmp(node_id);
    while currentIndex < 10 loop
        RAISE NOTICE 'currentIndex: %s', currentIndex;

        for nid, nrank in 
        select trans.to_id, (1 - damper)/num_of_nodes + damper * sum(trans.weight * %s.rank) 
        from trans, %s where trans.from_id = %s.node_id 
        group by trans.to_id loop
            update pagerank_tmp set rank = nrank where node_id = nid;        
        end loop;

        select sum( (N.rank - O.rank) * (N.rank - O.rank) ) into diff 
        from %s as O, pagerank_tmp as N where O.node_id = N.node_id;

        delete from %s;
        insert into %s select * from pagerank_tmp;

        currentIndex := currentIndex + 1;
        if diff < 0.0001 then
            exit;
        end if;
    end loop;
    drop table pagerank_tmp;
    drop table trans;
    drop table out_degree;
END;
$$
LANGUAGE plpgsql;
'''