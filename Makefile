.PHONY: test check up down

test:
	bash scripts/testar-tudo.sh

check:
	python3 scripts/revisar-arquivos.py

up:
	cd lab/01-linux-docker && docker compose up --build -d

down:
	cd lab/01-linux-docker && docker compose down
