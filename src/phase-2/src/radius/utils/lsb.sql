create or replace function lsb(bit)
returns int
AS
$$
declare
len int;
bitStr alias for $1;
tmpBit int;

BEGIN
	select length(bitStr) into len;
	for i in 1..len LOOP
		select get_bit(bitStr, len - i - 1) into tmpBit;
		if tmpBit = 1 then
			return i - 1; 
		end if;
	end loop;
END;
$$
language plpgsql