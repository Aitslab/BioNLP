init:
    pip install -r requirements.txt
	
	ifneq (,$(wildcard ./.env))
    	include .env
    	export
	endif
	
	pip install ACTIVATED_NLPMODEL_PATH
	
	


	echo $MY_ENV_VARIABLE
test:
    py.test tests
 #. .venv/bin/activate && py.test tests --cov=src --cov-report=term-missing --cov-fail-under 95
.PHONY: init test