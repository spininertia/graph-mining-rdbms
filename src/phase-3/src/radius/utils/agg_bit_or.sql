CREATE AGGREGATE agg_bit_or(bit[])
(
	sfunc = bit_or,
	stype = bit[]	
);