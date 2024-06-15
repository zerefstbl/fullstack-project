#!/bin/sh

stop_containers() {
    echo "\nStopping Docker containers..."
    docker-compose down
    echo "Containers stopped."
    exit 0
}

trap stop_containers INT

docker-compose build

docker-compose run --rm test

docker-compose run api
