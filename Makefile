develop:
	# python setup.py develop
	script/bootstrap

test:
	# python setup.py nosetests
	nosetests ./tests/
