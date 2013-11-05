create or replace function bit_or(BIT[], BIT[])
returns BIT[]
AS
$$
declare
bs1 ALIAS for $1;
bs2 ALIAS for $2;
retval BIT(16)[];
BEGIN
	for i in array_lower(bs1, 1)..array_upper(bs2, 1) LOOP
		retval[i] := bs1[i] | bs2[i];
	end loop; 
	return retval;
END;
$$
language plpgsql
STRICT