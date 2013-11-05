create or replace function fm_size(bit[])
returns numeric
AS
$$
declare
size numeric;
phi numeric := 0.77351;
bit_arr ALIAS for $1;
r int := 0;
k int := 0;
BEGIN
	for i in array_lower(bit_arr, 1)..array_upper(bit_arr, 1) loop
		r := r + lsb(bit_arr[i]);
		k = k + 1;
	end loop;
	raise notice '%', r;
	select power(2, 1.0 * r/k) / phi into size;
	return size;
END;
$$
language plpgsql;
