docker compose up -d
docker compose run --rm inventree-server invoke update

Om een extra admin aan te maken => docker compose run --rm inventree-server invoke superuser

Om container down te doen => docker compose down