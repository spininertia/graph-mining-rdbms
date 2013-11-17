create or replace function cc_main() returns void AS
$$
DECLARE
iter integer := 1;
diff_count integer := 0;
BEGIN
	perform init_component();
	perform update_component();
	select into diff_count count_diff();
	while diff_count > 0 loop
		RAISE NOTICE 'iteration: %, diff_count: %', iter, diff_count;
		perform assign();
		perform update_component();
		select into diff_count count_diff();
		iter := iter + 1;
	end loop;
	perform cc_stat();
END;
$$
language plpgsql;