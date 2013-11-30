all: install 

install:
	createdb mydb;
demo:
	cd src && nosetests -v  

paper.pdf:
	cd doc && make

clean:
	cd src && rm -r *.pyc

all.tar:
	tar czf graph_miner.tar.gz *
