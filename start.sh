#!/bin/sh

stop_containers() {
    echo "\nStopping Docker containers..."
    docker-compose down
    echo "Containers stopped."
    exit 0
}

trap stop_containers INT

docker-compose build

# 1. Iniciar o banco de dados
echo "Starting the databases..."
docker-compose up -d db db-test
echo "Databases started."

# Esperar até que os bancos de dados estejam prontos
echo "Waiting for the databases to be ready..."
until docker exec $(docker-compose ps -q db) pg_isready -U postgres; do
  sleep 1
done
until docker exec $(docker-compose ps -q db-test) pg_isready -U postgres; do
  sleep 1
done
echo "Databases are ready."

# 2. Rodar os testes
echo "Running tests..."
docker-compose run --rm test

# 3. Derrubar o container de teste e banco de teste
echo "Stopping test containers..."
docker-compose down db-test
echo "Test containers stopped."

# 4. Rodar o backend
echo "Starting the backend..."
docker-compose up -d api
echo "Backend started."

# Esperar até que o backend esteja pronto verificando a rota de health check
echo "Waiting for the backend to be ready..."
until curl -sf http://localhost:8000/; do
  echo "Adding pokemons..."
  sleep 20
done
echo "Backend is ready."

# 5. Rodar o frontend
echo "Starting the frontend..."
docker-compose up -d bo
echo "Frontend started."

# Para manter o script ativo até você interromper manualmente
tail -f /dev/null
