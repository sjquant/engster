migrations:
	docker-compose -f docker-compose.dev.yml run --rm engster_server /bin/sh -c \
	"python manage.py makemigrations"
	
dev-build:
	docker-compose -f docker-compose.dev.yml build && docker rmi $$(docker images -f "dangling=true" -q) -f

dev-migrate:
	docker-compose -f docker-compose.dev.yml run --rm engster_server /bin/sh -c \
	"python manage.py migrate"

dev-downgrade:
	docker-compose -f docker-compose.dev.yml run --rm engster_server /bin/sh -c \
	"python manage.py downgrade"
	
dev-init:
	docker-compose -f docker-compose.dev.yml run --rm engster_server /bin/sh -c \
	"python manage.py migrate && python manage.py init"

dev-log:
	docker-compose -f docker-compose.dev.yml logs -f $(service)

dev-up:
	docker-compose -f docker-compose.dev.yml up --build

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-ps:
	docker-compose -f docker-compose.dev.yml ps

dev-shell:
	docker-compose -f docker-compose.dev.yml run --rm engster_server /bin/sh

dev-clean:
	docker-compose -f docker-compose.dev.yml rm --stop --force -v