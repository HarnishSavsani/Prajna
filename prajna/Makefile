.PHONY: up down test verify smoke clean

up:
	docker compose -f docker-compose.prajna.yml up -d

down:
	docker compose -f docker-compose.prajna.yml down

verify:
	PYTHONPATH=. python prajna/verify.py

test:
	PYTHONPATH=. pytest prajna/tests

smoke:
	curl -s http://localhost:8080/health | grep '"status":"ok"'
