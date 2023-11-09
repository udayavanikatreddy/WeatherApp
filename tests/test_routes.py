import unittest
from datetime import datetime, timedelta, timezone

from flask import json

from app import app, db
from app.models import Measurement, Sensor


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        # Create an application context before creating tables
        with app.app_context():
            db.create_all()

        self.app = app.test_client()


    def tearDown(self):
        # Drop tables within the application context
        with app.app_context():
            db.session.remove()
            db.drop_all()


    def test01_create_measurement(self):
        with app.app_context():
            # Create a test sensor
            sensor = Sensor(name='Test Sensor', location='Test Location')
            db.session.add(sensor)
            db.session.commit()

            # Test creating a measurement with a valid timestamp
            timestamp = datetime.now(timezone.utc)  # Use a valid UTC timestamp
            measurement_data = {
                'sensor_id': sensor.id,
                'metric': 'temperature',
                'value': 25.0,
                'timestamp': timestamp.isoformat()  # ISO 8601 format
            }

            response = self.app.post('/measurements', json=measurement_data)
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['message'], 'Measurement created successfully')


    def test02_query_measurements(self):
        with app.app_context():
            # Create a test sensor
            sensor = Sensor(name='Test Sensor', location='Test Location')
            db.session.add(sensor)
            db.session.commit()

            # Create a test measurement
            measurement = Measurement(sensor_id=sensor.id, metric='temperature', value=25.0)
            db.session.add(measurement)
            db.session.commit()

            # Test querying measurements
            response = self.app.get('/measurements', query_string={
                'sensor_id': sensor.id,
                'metric': 'temperature',
                'statistic': 'avg',
                'start_date': '2023-01-01',
                'end_date': '2023-01-10'
            })

            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            print(data)


    def test03_query_by_sensor(self):
        with app.app_context():
            sensor = Sensor(name='Test Sensor', location='Test Location')
            db.session.add(sensor)
            db.session.commit()

            measurement = Measurement(sensor_id=sensor.id, metric='temperature', value=25.0)
            db.session.add(measurement)
            db.session.commit()

            response = self.app.get(f'/measurements?sensor_id={sensor.id}')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['results']), 1)

    def test_query_by_metric(self):
        with app.app_context():
            sensor = Sensor(name='Test Sensor', location='Test Location')
            db.session.add(sensor)
            db.session.commit()

            measurement = Measurement(sensor_id=sensor.id, metric='temperature', value=25.0)
            db.session.add(measurement)
            db.session.commit()

            response = self.app.get(f'/measurements?metric=temperature')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['results']), 1)

    def test_query_by_statistic(self):
        with app.app_context():
            sensor = Sensor(name='Test Sensor', location='Test Location')
            db.session.add(sensor)
            db.session.commit()

            measurement = Measurement(sensor_id=sensor.id, metric='temperature', value=25.0)
            db.session.add(measurement)
            db.session.commit()

            response = self.app.get(f'/measurements?sensor_id={sensor.id}&statistic=avg')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertIn('statistic', data)

    def test_query_by_date_range(self):
        with app.app_context():
            sensor = Sensor(name='Test Sensor', location='Test Location')
            db.session.add(sensor)
            db.session.commit()

            measurement = Measurement(sensor_id=sensor.id, metric='temperature', value=25.0)
            db.session.add(measurement)
            db.session.commit()

            start_date = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = datetime.utcnow().strftime('%Y-%m-%d')

            response = self.app.get(f'/measurements?sensor_id={sensor.id}&start_date={start_date}&end_date={end_date}')
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['results']), 1)

if __name__ == '__main__':
    unittest.main()
