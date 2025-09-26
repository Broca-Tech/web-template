.PHONY: up build prod-build start down status

# 開発サーバーを起動
up:
	docker compose up -d

build:
	docker compose build

# プロダクションビルド
prod-build:
	docker compose -f docker-compose.prod.yml build

# プロダクションサーバーを起動
start:
	docker compose -f docker-compose.prod.yml up -d

down:
	docker compose down

# サービスの状態を確認
status:
	docker compose ps