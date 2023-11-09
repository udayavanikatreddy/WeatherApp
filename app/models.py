from datetime import datetime

from app import db


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    metric = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'sensor_id': self.sensor_id,
            'metric': self.metric,
            'value': self.value,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }