import psycopg2

# user defined functions
def create_bit_or(conn):
	func_def = \
		'''
		create or replace function bit_or(BIT[], BIT[])
		returns BIT[]
		AS
		$$
		declare
		bs1 ALIAS for $1;
		bs2 ALIAS for $2;
		retval BIT(32)[];
		BEGIN
			for i in array_lower(bs1, 1)..array_upper(bs2, 1) LOOP
				retval[i] := bs1[i] | bs2[i];
			end loop; 
			return retval;
		END;
		$$
		language plpgsql
		STRICT
		'''
	create_function(conn ,func_def)

def create_agg_bit_or(conn):
	cur = conn.cursor()
	cur.execute("drop aggregate if exists agg_bit_or(bit[])")
	func_def = \
	'''
	CREATE AGGREGATE agg_bit_or(bit[])
	(
		sfunc = bit_or,
		stype = bit[]	
	);
	'''
	create_function(conn ,func_def)

def create_fm_assign(conn):
	func_def = \
	"""
	create or replace function fm_assign(int)
	returns BIT[]
	AS
	$$
	declare
	dim ALIAS for $1;
	retVal bit(32)[];
	bitStr bit(32);
	rndNum numeric;
	index int;
	BEGIN
		for i in 1..dim LOOP
			retVal[i] := 0::bit(32);
			select random() into rndNum;
			select floor(log(0.5, rndNum)) into index;
			select set_bit(retVal[i], index, 1) into bitStr;
			retVal[i] := bitStr;
			raise notice '% % %',bitStr, rndNum, index;
		end loop; 
		return retVal;
	END;
	$$
	language plpgsql
	"""
	create_function(conn ,func_def)

def create_fm_size(conn):
	func_def = \
	"""
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
			r := r + msb(bit_arr[i]);
			k = k + 1;
		end loop;
		raise notice '%', r;
		select power(2, 1.0 * r/k) / phi into size;
		return size;
	END;
	$$
	language plpgsql;
	"""
	create_function(conn ,func_def)

def create_msb(conn):
	func_def = \
	"""
	create or replace function msb(bit)
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
			select get_bit(bitStr, i - 1) into tmpBit;
			if tmpBit = 0 then
				return i; 
			end if;
		end loop;
	END;
	$$
	language plpgsql
	"""
	create_function(conn ,func_def)


def create_function(conn, func_def):
	cur = conn.cursor()
	cur.execute(func_def)
	cur.close()
	conn.commit()

def init_udf(conn):
	create_bit_or(conn)
	create_agg_bit_or(conn)
	create_msb(conn)
	create_fm_size(conn)
	create_fm_assign(conn)

if __name__ == '__main__':
	conn = psycopg2.connect(database="mydb", host="127.0.0.1")
	
	conn.close()