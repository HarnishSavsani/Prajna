.PHONY: up down restart logs ps build verify prajna-build build-prajna prajna-up up-prajna prajna-down down-prajna prajna-logs logs-prajna

# -----------------------------------------------------------------------------
# Prajna — Graph-Native AI Knowledge Engine (FalkorDB + Backend + Web)
# Built October 15–18, 2026 for FalkorDB Graph Hacks 2026
# -----------------------------------------------------------------------------

# Build with no cache and run Prajna
build: build-prajna
prajna-build: build-prajna
build-prajna:
	docker compose -p prajna -f docker-compose.prajna.yml build prajna-backend
	docker compose -p prajna -f docker-compose.prajna.yml build prajna-web
	docker compose -p prajna -f docker-compose.prajna.yml up -d --force-recreate

# Start Prajna stack
up: up-prajna
prajna-up: up-prajna
up-prajna:
	docker compose -p prajna -f docker-compose.prajna.yml up -d

# Stop Prajna stack
down: down-prajna
prajna-down: down-prajna
down-prajna:
	docker compose -p prajna -f docker-compose.prajna.yml down

# Restart Prajna services
restart:
	docker compose -p prajna -f docker-compose.prajna.yml restart

# Tail Prajna logs
logs: logs-prajna
prajna-logs: logs-prajna
logs-prajna:
	docker compose -p prajna -f docker-compose.prajna.yml logs -f

# Check Prajna container statuses
ps:
	docker compose -p prajna -f docker-compose.prajna.yml ps

# Run autonomous proof-of-life and verification test harness
verify:
	docker exec prajna-backend python3 /workspace/prajna/verify.py
