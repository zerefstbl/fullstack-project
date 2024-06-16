# Fullstack Project

This repository contains a complete fullstack project that combines an interactive frontend with an efficient and testable backend.

## Project Structure

The project structure is divided into two main parts, the frontend and the backend, in addition to configuration files and useful scripts:

```
fullstack-project/
├── backend/          # FastAPI code and tests
├── frontend/         # React + Redux code
├── .env              # Environment variables for production
├── .env.example      # Template for environment variables
├── .env.test         # Environment variables for testing
├── docker-compose.yml# Container orchestration with Docker Compose
└── start.sh          # Script to facilitate starting the application
```

It's worth noting that the environment variables would be omitted within a real-world project.

## Backend

The `backend` directory contains a FastAPI application built to be asynchronous, scalable, and easy to maintain. It uses Alembic for database migrations and SQLAlchemy as an ORM (Object-Relational Mapping) to interact with the database in a more intuitive and secure way.
An initial_data.py script was used to populate the database and persist the pokemon information so that it was not necessary to make requests to the external api
The script was built using async in conjunction with sempahores batches to create and other functions for better performance

### Testing

To ensure code quality and reliability, we use `pytest` to write and run automated tests. This allows us to verify that all functionalities are operating as expected before any updates are applied to the main codebase.

## Frontend

In the `frontend` directory, you will find a React application that uses Redux for state management. This combination provides a fluid and responsive user experience, allowing the application's state to be consistently maintained across all interactions.

## Getting Started

Follow the steps below to set up your environment and run the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/zerefstbl/fullstack-project.git
    cd fullstack-project
    ```

2. Set up the environment variables:
    ```bash
    cp .env.example .env
    # Edit the .env file with your specific settings
    ```

3. Use the `start.sh` script to start the application:
    ```bash
    sh start.sh
    ```

After running the script, the user interface will be available at `http://localhost:3000`, while the backend API can be accessed at `http://localhost:8000`.

### To view the documentation, simply access: `http://localhost:8000/docs`
![image](https://github.com/zerefstbl/fullstack-project/assets/102335897/91075849-955d-4917-a3f9-4bda5befca45)


## Employed Technologies

- **Frontend**: React + Redux for building dynamic interfaces and advanced state management.
- **Backend**: FastAPI for creating fast and efficient APIs, Alembic for database version control, SQLAlchemy as an ORM, and `pytest` for automated testing.
- **Infrastructure**: Docker and Docker Compose for simplified containerization and service orchestration.

## Backend json
All pokemons route
![image](https://github.com/zerefstbl/fullstack-project/assets/102335897/64879765-2646-4178-b99f-74085046492b)
Xml route
![image](https://github.com/zerefstbl/fullstack-project/assets/102335897/401b939e-dae1-4e2b-9bbf-d50f3b169f43)
Pokemon Details route
![image](https://github.com/zerefstbl/fullstack-project/assets/102335897/ba9db4b8-0536-4526-972b-52a7aa3da6b8)

## Frontend
![image](https://github.com/zerefstbl/fullstack-project/assets/102335897/4bbbacc1-7899-4518-b694-9ee94564ce27)
![image](https://github.com/zerefstbl/fullstack-project/assets/102335897/790ea2c2-893a-42f5-ab5f-5f27df2bd1b2)
