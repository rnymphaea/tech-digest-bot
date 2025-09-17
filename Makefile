BOT_SERVICE=bot 

.PHONY: all
all: build up

.PHONY: build
build:
	docker compose build

.PHONY: up 
up:
	docker compose up -d

.PHONY: down 
down:
	docker compose down
