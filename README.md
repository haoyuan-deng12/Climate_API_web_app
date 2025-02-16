# Climate Action App

A robust Flask-based web application that provides real-time climate data monitoring and analysis. The app seamlessly integrates external APIs, displays query results on web pages, and stores returned data in MongoDB for persistent historical records.
(Note: Some features are not implemented yet, mainly focusing on completed external API query, and MongoDB storage)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Setup](#database-setup)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [External Integrations](#external-integrations)
- [Security & Logging](#security--logging)
- [License](#license)

---

## Overview

Climate Action App is a Flask-powered web application designed to monitor climate-related data. The app integrates with multiple external APIs to fetch data—such as weather forecasts, global fire information, and oil slick detection—and immediately displays the results on the user interface. Moreover, the application stores the fetched data into MongoDB, ensuring that historical records are maintained for further analysis.

---

## Features

  
- **Location Alerts:**  
  - Submit and view alerts with precise geographical coordinates and custom messages.


- **Query API Results Display:** 
  - **Implemented Feature:** Users can query external APIs (Open-Meteo, NASA FIRMS, Cerulean) and view the returned data immediately on the web pages.  
  - **Real-Time Data:** API query results such as climate forecasts, fire data, and oil slick detections are dynamically fetched and rendered.


- **Data Persistence in MongoDB:**  
  - **Implemented Feature:** The application processes and stores the results returned from external API calls into MongoDB collections. This includes weather data, global fire data, and oil slick detection records, ensuring historical data is available for analysis.


- **Responsive UI:**  
  - Built using Bootstrap 5 for a clean and responsive design that works across all devices.


- **Logging & Debugging:**  
  - Extensive logging captures user activities and API interactions, with logs stored in a dedicated `logs.log` file.

---

## Project Structure

```
(Note: Some features are not implemented yet, mainly focusing on completed external API query, and MongoDB storage)
Climate Action App/
├── app.py                 # Main Flask application (routes, DB initialization, API endpoints)
├── static/
│   ├── main.js            # JavaScript for dynamic API calls and data rendering
│  
├── templates/
│   ├── base.html          # Base template with navigation and common layout
│   ├── home.html          # Homepage template
│   ├── users.html         # User registration and listing template
│   ├── alerts.html        # Location alerts submission and listing template
│   ├── dashboard.html     # Climate dashboard template displaying statistics
│   ├── external_api.html  # Template for interacting with external APIs and displaying results
│   ├── quiz.html          # Climate quiz page
│   ├── world_map.html     # Interactive world map template
│   
├── logs.log               # Log file recording user activity and API interactions
├── requirements.txt       # Python dependencies for the project
└── README.md              # Project documentation (this file)
```

---

## Database Setup

The application utilizes **two types of databases**:

1. **SQL Database (SQLite):**  
   - **Purpose:**  
     Stores structured data such as user records, location alerts, and climate issues.
   - **Configuration:**  
     Utilizes SQLAlchemy with a SQLite database file named `climate_app.db`.
   - **Models:**  
     - **User:** Stores user IDs, usernames, and roles.
     - **LocationAlert:** Contains alerts with latitude, longitude, and custom messages.
     - **ClimateIssue:** Records climate issues with details like country, issue description, and severity.
   - **Initialization:**  
     Tables are auto-created on startup using `db.create_all()`.

2. **NoSQL Database (MongoDB):**  
   - **Purpose:**  
     Used to persist external API data for dynamic datasets.
   - **Configuration:**  
     Connects to a local MongoDB server (`mongodb://localhost:27017/`) and uses a database named `local`.
   - **Collections:**  
     - **fireData:** Stores global fire data fetched from the NASA FIRMS API.
     - **weatherData:** Stores climate forecast data retrieved from the Open-Meteo API.
     - **oilData:** Stores oil slick detection data from the Cerulean API.
   - **Data Insertion:**  
     Fetched API results are processed and inserted into respective MongoDB collections to maintain historical records.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/climate-action-app.git
   cd climate-action-app
   ```

2. **Set Up a Virtual Environment and Install Dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment:**

   - Ensure that MongoDB is installed and running locally.
   - Adjust configuration variables as needed within the code or via environment settings.

4. **Database Initialization:**

   The application auto-creates necessary tables on startup. For production use, consider database migrations with Alembic.

---

## Usage

1. **Run the Application:**

   ```bash
   python app.py
   ```

   The app runs in debug mode on port 5000 (access via [http://127.0.0.1:5000](http://127.0.0.1:5000)).

2. **Access the Application:**

   - **Homepage:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - **User Management:** [http://127.0.0.1:5000/users](http://127.0.0.1:5000/users)
   - **Location Alerts:** [http://127.0.0.1:5000/alerts](http://127.0.0.1:5000/alerts)
   - **Climate Dashboard:** [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard)
   - **Climate Quiz:** [http://127.0.0.1:5000/quiz](http://127.0.0.1:5000/quiz)
   - **Interactive World Map:** [http://127.0.0.1:5000/world_map](http://127.0.0.1:5000/world_map)
   - **External API Data:** [http://127.0.0.1:5000/external_api](http://127.0.0.1:5000/external_api)

3. **Front-End Interactions:**

   - API query results for climate data, fire data, and oil slick detections are dynamically fetched and displayed on their respective pages.
   - The fetched data is stored in MongoDB for future reference, ensuring that historical data is preserved.

---

## API Endpoints

- **GET /climate_data:**  
  Retrieves a 16-day climate forecast for a specified latitude and longitude using the Open-Meteo API.  
  **Display:** Results are rendered on the external API data page and stored in the MongoDB `weatherData` collection.

- **GET /fire_data:**  
  Fetches global fire data from NASA FIRMS API with parameters for country, data source, and day range.  
  **Display:** Data is displayed on the external API page and persisted in the MongoDB `fireData` collection.

- **GET /spill_data_oil:**  
  Queries oil slick detection data from the Cerulean API, accepting bounding box, start/end dates, minimum confidence, and result limit.  
  **Display:** Query results are shown on the external API page and stored in the MongoDB `oilData` collection.

- **Other Routes:**  
  Additional routes provide HTML-rendered pages for user registration, location alerts, dashboards, quizzes, and interactive maps.

---

## External Integrations

- **Open-Meteo API:**  
  Supplies weather forecast data (daily max/min temperatures, timezone, etc.) for a 16-day period.

- **NASA FIRMS API:**  
  Provides global fire data, which is parsed and stored in MongoDB.

- **Cerulean API:**  
  Detects oil slicks using machine learning; results are processed, displayed, and stored for environmental monitoring.

---

## Security & Logging

- **Security Measures:**  
  - Comprehensive input validations across all forms.
  - Error handling and rate limiting implemented for API endpoints to prevent misuse.
  
- **Logging:**  
  - Significant user activities and API interactions are logged in `logs.log` for audit and debugging purposes.
  - Debug messages, including constructed API URLs, are printed to the console to aid troubleshooting.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

