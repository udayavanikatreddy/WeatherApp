from flask import jsonify, request

from app import app, db
from app.models import Measurement, Sensor
from app.utils import calculate_statistic


@app.route('/measurements', methods=['POST'])
def create_measurement():
    data = request.get_json()

    # Validate required fields
    if 'sensor_id' not in data or 'metric' not in data or 'value' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate sensor_id is a positive integer
    try:
        sensor_id = int(data['sensor_id'])
        if sensor_id <= 0:
            raise ValueError()
    except ValueError:
        return jsonify({'error': 'Invalid sensor_id. Must be a positive integer'}), 400

    # Validate metric is a non-empty string
    if not isinstance(data['metric'], str) or not data['metric']:
        return jsonify({'error': 'Invalid metric. Must be a non-empty string'}), 400

    # Validate value is a float
    try:
        value = float(data['value'])
    except ValueError:
        return jsonify({'error': 'Invalid value. Must be a numeric value'}), 400

    new_measurement = Measurement(sensor_id=sensor_id, metric=data['metric'], value=value)
    db.session.add(new_measurement)
    db.session.commit()

    return jsonify({'message': 'Measurement created successfully'}), 201


@app.route('/measurements', methods=['GET'])
def query_measurements():
    query_params = request.args.to_dict()

    # Validate required parameters
    if 'sensor_id' not in query_params:
        return jsonify({'error': 'Missing required parameter: sensor_id'}), 400

    try:
        sensor_id = int(query_params['sensor_id'])
        if sensor_id <= 0:
            raise ValueError()
    except ValueError:
        return jsonify({'error': 'Invalid sensor_id. Must be a positive integer'}), 400

    # Build query based on parameters
    query = db.session.query(Measurement)

    query = query.filter(Measurement.sensor_id == sensor_id)

    if 'metric' in query_params:
        query = query.filter(Measurement.metric == query_params['metric'])

    if 'start_date' in query_params:
        start_date = query_params['start_date']
        query = query.filter(Measurement.timestamp >= start_date)

    if 'end_date' in query_params:
        end_date = query_params['end_date']
        query = query.filter(Measurement.timestamp <= end_date)

    # Execute query and calculate statistic
    results = query.all()

    # Calculate statistic (e.g., average value)
    statistic = calculate_statistic(results, query_params.get('statistic'))

    # Return results
    return jsonify({'results': [measurement.to_dict() for measurement in results], 'statistic': statistic}), 200
