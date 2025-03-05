# Climate & Environmental Data Dashboard

This project is a full-stack application built using Flask, SQLAlchemy, and MongoDB. It aggregates environmental data such as climate forecasts, global fire data, and oil slick detections. The frontend is powered by HTML, CSS, and JavaScript while the backend integrates with external APIs to fetch and store data.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Frontend Usage](#frontend-usage)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application provides:
- **User Management:** Registration and role-based access (admin or user).
- **Climate Dashboard:** Display and analysis of climate issues and severity.
- **Interactive Maps:** Visualize climate issues on a world map.
- **External Data Integration:** Retrieve real-time data from:
    - **Open-Meteo Climate API:** For temperature forecasts.
    - **NASA FIRMS API:** For global fire data.
    - **Cerulean API:** For oil slick detection data.
- **Quiz Feature:** An interactive quiz to test users’ knowledge of environmental issues.

## Features

- **Flask Backend:** RESTful endpoints and traditional template rendering.
- **SQLAlchemy with SQLite:** Manage user, alerts, and climate issues data.
- **MongoDB Integration:** Store fetched external data such as fire and oil slick data.
- **Dockerized Environment:** Containerized application for easy deployment.
- **Frontend Components:** HTML templates with JavaScript to fetch and display external API data.

## Project Structure

```
.
├── app.py                  # Main Flask application, routes and database models
├── Dockerfile              # Dockerfile for building the application image
├── docker-compose.yml      # Docker Compose file for multi-container setup (Flask app + MongoDB)
├── main.js                 # JavaScript file for fetching and displaying API data
├── home.html               # Minimal homepage template
├── external_api.html       # Template for interacting with external API data
└── base.html               # Base template (assumed to be present in the templates directory)
```

**Detailed Code Comments:**
- Every route and function in `app.py` includes detailed inline comments explaining its purpose and behavior.
- JavaScript functions in `main.js` include detailed commentary to explain how data is fetched, processed, and rendered in the browser.

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://your-repo-url.git
   cd your-repo-directory
   ```

2. **Install Dependencies:**
   Make sure you have Python 3 installed. Then, create a virtual environment and install the required packages:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   > *Note:* The `requirements.txt` should include dependencies such as Flask, SQLAlchemy, PyMongo, and requests.

3. **MongoDB Setup:**
   If not using Docker, install MongoDB locally or configure the environment variable `MONGO_URI` with your MongoDB connection string.

## Running the Application

### Without Docker
1. **Initialize the Database:**
   The tables are created automatically when the application starts. If needed, you can manually trigger the database initialization by running:
   ```bash
   python app.py
   ```

2. **Run the Flask App:**
   ```bash
   flask run
   ```
   The application should be accessible at `http://127.0.0.1:5000/`.

### With Docker

1. **Build and Run Containers:**
   Make sure Docker and Docker Compose are installed. Then run:
   ```bash
   docker-compose up --build
   ```
   This command builds the Flask application image and starts both the app and MongoDB services. The app is mapped to port 5000 on your host.

2. **Access the Application:**
   Navigate to `http://localhost:5000/` to view the dashboard.

## API Endpoints

Below are some key API endpoints provided by the application:

- **Home Page:**
    - `GET /`  
      Renders the homepage.

- **User Management:**
    - `GET, POST /users`  
      Display user list or register a new user.

- **Location Alerts:**
    - `GET, POST /alerts`  
      Display alerts or add a new location alert.

- **Climate Dashboard:**
    - `GET /dashboard`  
      Display the climate dashboard with aggregated statistics.

- **Quiz:**
    - `GET, POST /quiz`  
      Serve quiz questions and process submissions.

- **World Map:**
    - `GET /world_map`  
      Render a page with an interactive world map of climate issues.

- **External API Data:**
    - `GET /external_api`  
      Renders a page to fetch climate API data.
    - `GET /climate_data`  
      Retrieves climate forecast data using the Open-Meteo API.
    - `GET /fire_data`  
      Retrieves global fire data from the NASA FIRMS API.
    - `GET /spill_data_oil`  
      Retrieves oil slick detection data from the Cerulean API.

Each endpoint includes detailed logging and error handling to ensure a smooth data retrieval process.

## Frontend Usage

- **Climate Data Query:**
  The `external_api.html` page allows users to input latitude and longitude values to fetch climate forecast data. Results are displayed dynamically in an HTML table.

- **Fire Data and Oil Slick Detection:**
  Forms on the `external_api.html` page allow querying and displaying fire data and oil slick detection results. Data is rendered in neatly formatted tables for easy viewing.

## Docker Deployment

The `docker-compose.yml` file defines two services:
- **app:** The Flask application which builds the image from the local Dockerfile.
- **mongodb:** The MongoDB database using the official image.

The services are connected using Docker Compose, with the MongoDB service exposed to the Flask app via the `MONGO_URI` environment variable.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


