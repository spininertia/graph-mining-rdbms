create or replace function fm_assign(int)
returns BIT[]
AS
$$
declare
dim ALIAS for $1;
retVal bit(16)[];
bitStr bit(16);
rndNum numeric;
index int;
BEGIN
	for i in 1..dim LOOP
		retVal[i] := 0::bit(16);
		select random() into rndNum;
		select floor(log(0.5, rndNum)) into index;
		if index >= 16 then
			index := 15
		end
		select set_bit(retVal[i], index, 1) into bitStr;
		retVal[i] := bitStr;
		raise notice '% % %',bitStr, rndNum, index;
	end loop; 
	return retVal;
END;
$$
language plpgsql