Coding Challenge
=================

Application Requirements
------------------------
Imagine that we are building a service that receives weather data from various sensors that report metrics such as temperature, humidity, wind speed, etc. Your task in this coding challenge is building an application that solves part of this problem:
    • The application can receive new metric values as the weather changes around the sensor via an API call.
    • The application must allow querying sensor data. A query should define:
    • One or more (or all sensors) to include in results.
    • The metrics (e.g. temperature and humidity); the application should return the average value for these metrics.
    • The statistic for the metric: min, max, sum or average.
    • A date range (between one day and a month, if not specified, the latest data should be queried).

    • Example query: Give me the average temperature and humidity for sensor 1 in the last week.

Technical Requirements
-----------------------
    • This application should be a REST API (no UI needed).
    • The programming language should preferably be Python, Java, JavaScript/TypeScript. There are no other restrictions on libraries or technologies.
    • The source code must be shared in a public repository: GitHub, Bitbucket, etc.
    (Please make the repository name a random string and avoid references to Genesys to prevent others copying your code in the future.)
    • The application data must be persisted in some kind of database/storage.
    • Include input validation and exception handling, as and where you find necessary.

Other Notes
------------
    • We do not expect you to spend more than a few hours on this challenge. Consider this a proof of concept. Not everything has to be perfect. If you don't have time to finish everything, please explain which parts are incomplete.
    • Documentation is nice to have but not required.
    • Implement unit/integration testing as you find necessary while building the application. We don't expect complete test coverage.
    • Include instructions on how to run, or anything that we should note on your approach in a README file.
    • If you have questions or clarifications, please contact your recruiter.
    • During the technical interview, we will be discussing the code you submitted, so be prepared to talk in-depth about the implementation, enhancements, etc.



## Requirements
    - REST API to receive and query weather sensor data
    - Store metrics like temperature, humidity, wind speed
    - Query by:
        - Sensor(s)
        - Metric(s)
        - Statistic (min, max, avg, sum)
        - Date range

Implementation
    Framework   : Flask (Python)
    Database    : SQLite
    Models:
        Sensor      - id, name, location
        Measurement - timestamp, sensor_id, metric, value
    API Routes:
        POST /measurements - create new measurement
        GET /measurements - query measurements

Input Validation:
    Sensor ID, metrics, stats, date range

# Weather API

## Setup
In Linux, 
    Give executable permissions for start.sh script
        $ chmod +x start.sh
    Run the start.sh shell script
        $ ./start.sh

In Windows, 
    Run the start.bat bash script
        $ start.bat

## Usage
1. Run the application: `python run.py`
2. Access the API at `http://127.0.0.1:5000/`

## API Endpoints
- **POST /measurements:** Create a new measurement.
- **GET /measurements:** Query measurements based on parameters.

## Testing
Run unit tests:
```bash
python -m unittest tests.test_routes

## Request - responses
- 
    GET http://127.0.0.1:5000/measurements
    Response
        {
            "error": "Missing required parameter: sensor_id"
        }

    GET http://127.0.0.1:5000/measurements?sensor_id=-2
    Response
        {
            "error": "Invalid sensor_id. Must be a positive integer"
        }

    GET http://127.0.0.1:5000/measurements?sensor_id=22
    Response
        {
            "results": [],
            "statistic": null
        }

    GET http://127.0.0.1:5000/measurements?sensor_id=22.3
    Response
        {
            "error": "Invalid sensor_id. Must be a positive integer"
        }

    GET http://127.0.0.1:5000/measurements?sensor_id=22&start_date=2023-11-01
    Response
        {
        "results": [],
        "statistic": null
        }
