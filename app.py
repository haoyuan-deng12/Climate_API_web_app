from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from urllib.parse import quote

from pyexpat import features
from pymongo import MongoClient
from sqlalchemy import Integer

app = Flask(__name__)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "climate_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----- MongoDB Setup -----
# Connect to local MongoDB server
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
# Use (or create) a database; here we use "fireDB" for example
mango_db = client["local"]
# Use (or create) a collection named "fireData"
fire_collection = mango_db["fireData"]
weather_collection = mango_db["weatherData"]
oil_collection = mango_db["oilData"]

# --------------------------------------------------------------------------
# Database Models
# --------------------------------------------------------------------------
class User(db.Model):
    """
    User model stores:
    - id: Unique user ID
    - username: User's name
    - role: 'admin' or 'user'
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')


class LocationAlert(db.Model):
    """
    LocationAlert model stores:
    - id: Unique ID
    - latitude, longitude: Coordinates
    - alert_message: The unique alert triggered at this location
    """
    __tablename__ = 'location_alerts'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    alert_message = db.Column(db.String(200), nullable=False)


class ClimateIssue(db.Model):
    """
    ClimateIssue model stores:
    - id: Unique ID
    - country: Country name or region
    - issue_description: Description of the climate issue
    - severity: A numeric severity level for demonstration
    """
    __tablename__ = 'climate_issues'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    issue_description = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.Integer, default=1)


# --------------------------------------------------------------------------
# Database Initialization
# --------------------------------------------------------------------------
with app.app_context():
    db.create_all()
    """
    Create tables before the first request.
    In a production environment, you might use Alembic migrations.
    """


# --------------------------------------------------------------------------
# Utility / Helper Functions
# --------------------------------------------------------------------------
def is_admin(user_id):
    """
    Utility to check if the user is an admin.
    Returns True if user's role is 'admin', otherwise False.
    """
    user = User.query.get(user_id)
    return (user and user.role == 'admin')


# --------------------------------------------------------------------------
# Routes - Traditional Flask Routes (Render Templates)
# --------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')


# ------------------- User Management -------------------
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # Handle user registration form submission
        username = request.form.get('username')
        role = request.form.get('role', 'user')

        if not username:
            return render_template('users.html', error="Username is required.")

        # Check if user already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            return render_template('users.html', error="User already exists.")

        new_user = User(username=username, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('users'))

    if request.method == 'GET':
        # GET request, display user list
        users = User.query.all()
        return render_template('users.html', users=users)


# ------------------- Location Alerts -------------------
@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    if request.method == 'POST':
        # Process location alert form submission
        try:
            lat = float(request.form.get('latitude'))
            lng = float(request.form.get('longitude'))
            msg = request.form.get('alert_message')

            if None in (lat, lng, msg) or not msg:
                return render_template('alerts.html', error="All fields are required.")

            alert = LocationAlert(latitude=lat, longitude=lng, alert_message=msg)
            db.session.add(alert)
            db.session.commit()
            return redirect(url_for('alerts'))
        except ValueError:
            return render_template('alerts.html', error="Invalid latitude or longitude.")

    # GET request, display alerts list
    alerts = LocationAlert.query.all()
    return render_template('alerts.html', alerts=alerts)


# ------------------- Climate Dashboard -------------------
@app.route('/dashboard')
def dashboard():
    """
    Render the climate dashboard with statistics.
    """
    total_issues = ClimateIssue.query.count()
    issues = ClimateIssue.query.all()
    if issues:
        avg_severity = sum(i.severity for i in issues) / len(issues)
    else:
        avg_severity = 0
    return render_template('dashboard.html', total_issues=total_issues, average_severity=round(avg_severity, 2))


# ------------------- Quiz -------------------
@app.route('/quiz', methods=['GET', 'POST'])
def quiz_page():
    if request.method == 'POST':
        # Process quiz submission
        # Add grading logic here
        return redirect(url_for('quiz_page'))

    # Provide quiz questions
    sample_quiz = [
        {
            "question": "Which gas is primarily responsible for global warming?",
            "options": ["CO2", "O2", "N2", "H2"],
            "correct_answer": "CO2"
        },
        {
            "question": "Which country has the highest CO2 emissions?",
            "options": ["China", "USA", "India", "Russia"],
            "correct_answer": "China"
        }
    ]
    return render_template('quiz.html', quiz=sample_quiz)


# ------------------- Interactive World Map -------------------
@app.route('/world_map')
def world_map():
    """
    Render a page with an interactive world map displaying climate issues.
    """
    issues = ClimateIssue.query.all()
    # Assume a dictionary that maps countries to coordinates
    country_coords = {
        "UK": (51.5074, -0.1278),
        "USA": (37.0902, -95.7129),
        "China": (35.8617, 104.1954),
        "India": (20.5937, 78.9629)
        # ... add more if needed
    }
    output = []
    for i in issues:
        lat, lng = country_coords.get(i.country)
        output.append({
            "country": i.country,
            "lat": lat,
            "lng": lng,
            "issue": i.issue_description,
            "severity": i.severity
        })
    return render_template('world_map.html', issues=output)


# --------------------------------------------------------------------------
# Routes - External API Usage (Render Template)
# --------------------------------------------------------------------------
@app.route('/external_api', methods=['GET'])
def external_api():
    """
    Render the External API Data page.
    """
    return render_template('external_api.html')


# --------------------------------------------------------------------------
# Routes - External API Usage (Keep as API Endpoint)
# --------------------------------------------------------------------------
@app.route('/climate_data', methods=['GET'])
def external_data():
    """
    Fetches climate data for a specified location using the Open-Meteo Climate API.
    Query parameters:
    - latitude: Latitude of the location.
    - longitude: Longitude of the location.

    The API request uses:
    - forecast_days=16
    - daily=temperature_2m_max,temperature_2m_min
    - timezone=Europe/London
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not all([latitude, longitude]):
        return jsonify({"error": "Missing required query parameters"}), 400

    api_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&forecast_days=16"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=Europe/London"
    )

    print(f"Constructed API URL: {api_url}")  # For debugging

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # ----- Insert the fetched fire data into MongoDB -----
        # This will store each dictionary in the "fireData" collection as a separate document.
        # Check if we have data to insert

        # --------------------------------------------------------

        result = []
        dates = data['daily']['time']
        max_tems = data['daily']['temperature_2m_max']
        min_tems = data['daily']['temperature_2m_min']
        for date, max_tem, min_tem in zip(dates, max_tems, min_tems):
            result.append({
                "Date": date,
                "Max_Temp (°C)": max_tem,
                "Min_Temp (°C)": min_tem
            })

        if result:
            weather_collection.insert_many(result)

        for record in result:
            if record['_id']:
                record['_id'] = str(record['_id'])

        return jsonify({
            "message": "Climate data fetched successfully",
            "data": data
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch climate data from Open-Meteo API",
            "details": str(e)
        }), 500


@app.route('/fire_data', methods=['GET'])
def fire_data():
    """
    Fetches global fire data from the NASA FIRMS API using the user's MAP_KEY.
    Query parameters:
    - country: 3-character ISO country code (e.g., USA for United States).
    - source: Data source, e.g., VIIRS_SNPP_NRT.
    - day_range: Number of days (1-10).
    """
    country = request.args.get('country', 'USA')  # Default value is 'USA'
    source = request.args.get('source', 'VIIRS_SNPP_NRT')  # Default data source
    day_range = request.args.get('day_range', '1')  # Default range is 1 day
    map_key = "f50171820302d881e6774d8dc41c20bc"  # Provided MAP_KEY
    display_number = request.args.get('display_number', 25)

    # Check if required parameters are valid
    if not all([country, source, day_range]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Construct API URL
    api_url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/"
        f"{map_key}/{source}/{country}/{day_range}"
    )

    print(api_url)

    try:
        # Send request
        response = requests.get(api_url, timeout=40)
        response.raise_for_status()

        # Split lines
        lines = response.text.strip().split("\n")  # ---> Output: "Hello, world!\nThis is a test.\nPython is great!"
        # Extract only the first 20 rows and required columns
        result = []
        for line in lines[1:int(display_number)+1]:
            row = line.split(",")
            result.append({
                "latitude": row[1],  # Fire location coordinates.
                "longitude": row[2],
                "bright_ti4": row[3],  # Brightness value (bright_ti4).
                "acq_date": row[6],  # Fire detection date.
                "frp": row[13]  # Fire Radiative Power (heat energy emitted).
            })

        # ----- Insert the fetched fire data into MongoDB -----
        # This will store each dictionary in the "fireData" collection as a separate document.
        new_result = []
        for waiting_to_insert_record in result:
            if fire_collection.find_one({'latitude': waiting_to_insert_record['latitude']}) is None:
                new_result.append(waiting_to_insert_record)

        if new_result:
            fire_collection.insert_many(new_result)

        for inserted_new_record in new_result:
            inserted_new_record['_id'] = str(inserted_new_record['_id'])

        # --------------------------------------------------------

        return jsonify({
            "message": "Global fire data fetched successfully",
            "data": result
        }), 200
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch fire data",
            "details": str(e)
        }), 500
    # OPTIONAL
    except IndexError as e:
        return jsonify({
            "error": "Data processing error",
            "details": str(e)
        }), 500


@app.route('/spill_data_oil', methods=['GET'])
def oil_spill_data():
    """
    Fetches oil slick detection data from the Cerulean API.

    Query parameters:
    - bbox: Bounding box in the format "xmin,ymin,xmax,ymax". Default: "10.9,42.3,19.7,36.1"
    - start_date: Start datetime in UTC (format: YYYY-MM-DDTHH:MM:SSZ). Default: "2024-09-01T00:00:00Z"
    - end_date: End datetime in UTC (format: YYYY-MM-DDTHH:MM:SSZ). Default: "2024-10-01T00:00:00Z"
    - min_confidence: Minimum machine confidence threshold. Default: "0.95"

    Note: The machine_confidence field represents the confidence score output by the machine learning model.
          A higher score indicates higher confidence that the detection is a true oil slick.
    """
    # Retrieve query parameters with defaults
    bbox = request.args.get('bbox').replace(" ", "")
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_confidence = request.args.get('min_confidence')
    limit = request.args.get("limit")

    # Build the filter string for machine_confidence
    filter_str = f"machine_confidence GTE {min_confidence}"
    encoded_filter = quote(filter_str)

    api_url = (
        f"https://api.cerulean.skytruth.org/collections/public.slick_plus/items"
        f"?limit={limit}"
        f"&bbox={bbox}"
        f"&datetime={start_date}/{end_date}"
        f"&sortby=-machine_confidence"
        f"&filter={encoded_filter}"
    )

    print("Constructed API URL:", api_url)

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # id area machine_confidence  slick_timestamp

        # Extract key properties from each slick detection
        slicks = []
        features = data.get("features")  # features is a list
        for item in features:
            property = item.get('properties')
            slicks.append({
                "id": property.get('id'),
                "area": property.get("area"),
                "machine_confidence": property.get("machine_confidence"),
                "slick_timestamp": property.get("slick_timestamp"),
                "classification": property.get("cls_long_name")  # Add this line
            })

        new_slicks = []
        for waiting_to_insert_slick in slicks:
            if oil_collection.find_one({"id": waiting_to_insert_slick['id']}) is None:
                new_slicks.append(waiting_to_insert_slick)

        if len(new_slicks) > 0:
            oil_collection.insert_many(new_slicks)

        return jsonify({
            "message": "Slick data fetched successfully",
            "data": slicks,
            "numberMatched": data.get("numberMatched"),
            "numberReturned": data.get("numberReturned")
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to fetch slick data",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "Data processing error",
            "details": str(e)
        }), 500


# --------------------------------------------------------------------------
# Main Entry
# --------------------------------------------------------------------------
if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
