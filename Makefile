install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# test:
# 	pytest -vv test_*.py

lint:
	pylint --disable=R,C,E0602,E1120 main.py my_lib/*.py

format:
	black *.py my_lib/*.py

deploy:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 354918363202.dkr.ecr.us-east-1.amazonaws.com
	docker build -t wikipedia .
	docker tag wikipedia:latest 354918363202.dkr.ecr.us-east-1.amazonaws.com/wikipedia:latest
	docker push 354918363202.dkr.ecr.us-east-1.amazonaws.com/wikipedia:latest
	
all: install lint format