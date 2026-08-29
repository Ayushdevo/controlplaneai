api:
	cd apps/api && uvicorn app.main:app --reload --port 8000

web:
	cd apps/web && npm run dev

compose-up:
	docker compose up --build

compose-down:
	docker compose down

api-test:
	cd apps/api && pytest
