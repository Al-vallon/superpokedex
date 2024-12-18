# Pokedex Application

## Description

This is a Pokedex application built using Django. The app allows users to browse, search, and view detailed information about different Pokémon. It includes features such as filtering Pokémon by type, abilities, and other characteristics. The application is designed to be run in a Docker container for easy deployment and portability.

## Features

- Browse a list of Pokémon.
- Filter Pokémon by type, ability, and other attributes.
- View detailed information about each Pokémon.
- API endpoints for interacting with Pokémon data.
- Dockerized for easy setup and deployment.

## Installation

### Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (optional but recommended)

### Running the Application

To run the Pokedex application locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/pokedex.git
  # Pokedex Application

## Description

This is a Pokedex application built using Django. The app allows users to browse, search, and view detailed information about different Pokémon. It includes features such as filtering Pokémon by type, abilities, and other characteristics. The application is designed to be run in a Docker container for easy deployment and portability.

## Features

- Browse a list of Pokémon.
- Filter Pokémon by type, ability, and other attributes.
- View detailed information about each Pokémon.
- API endpoints for interacting with Pokémon data.
- Dockerized for easy setup and deployment.

## Installation

### Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (optional but recommended)

### Running the Application

To run the Pokedex application locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/pokedex.git
2. Build and run the Docker container:

If you're using Docker Compose, you can build and run the container by executing:

   docker-compose up --build
   
3. Access the application:

Once the container is running, you can access the application by navigating to http://localhost:8000 in your web browser.

4. Apply database migrations:

If you're running the application for the first time, you need to apply the database migrations. You can do this by running the following command inside the Docker container:

docker exec -it pokedex_container_name python manage.py migrate




