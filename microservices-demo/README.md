# microservices_demo

A tiny, fully‑functional micro‑service stack that demonstrates:

* **User service** – registration, login, JWT authentication
* **Inventory service** – CRUD for products
* **Order service** – create orders (simple)
* **API Gateway** – forwards all `/api/*` requests
* **Airflow** – a trivial DAG that prints a line

## Getting started

```bash
# clone the repo (or copy the folder tree above)
git clone https://github.com/<your‑org>/microservices_demo
cd microservices_demo
docker-compose up --build