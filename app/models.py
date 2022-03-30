from app import db
from datetime import datetime

class Inspection(db.Model):
    inspection_id = db.Column(db.Integer, primary_key=True)
    inspection_date = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(2048))
    insert_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))
    violations = db.relationship('Violation', backref='violation_log', lazy='dynamic')

    cols = ['inspection_id', 'inspection_date', 'score', 'comments', 'restaurant']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return('Inspection {}'.format(self))
    
    def to_dict(self):
        data = {
            'inspection_id': self.inspection_id,
            'inspection_date': self.inspection_date,
            'score': self.score,
            'comments': self.comments
        }
        return data
    
    # need to grab the restaurant_id key so can capture FK relationship
    def from_dict(self, data):
        for col in self.cols:
            if col in data:
                if col == 'restaurant':
                    setattr(self, 'restaurant_id', data[col]['restaurant_id'])
                else:
                    setattr(self, col, data[col])

class Restaurant(db.Model):
    # Restaurant information for inspections data
    restaurant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    street_address = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    insert_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cuisine_type = db.Column(db.String(64), nullable=True)

    inspections = db.relationship('Inspection', backref='inspections_log', lazy='dynamic')

    cols = ['restaurant_id', 'name', 'city', 'street_address', 'state', 'postal_code', 'insert_timestamp', 'cuisine_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return('Restaurant {}'.format(self))

    def to_dict(self):
        data = {
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'city': self.city,
            'street_address': self.street_address,
            'state': self.state,
            'postal_code': self.postal_code
        }
        if self.cuisine_type not in ['', None]:
            data['cuisine_type'] = self.cuisine_type
        
        return data

    def from_dict(self, data):
        for col in self.cols:
            if col in data:
                setattr(self, col, data[col])

class Violation(db.Model):
    violation_id = db.Column(db.Integer, primary_key=True)
    is_critical = db.Column(db.Boolean, nullable=False)
    code = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    comments = db.Column(db.String(2048), nullable=False)

    # optional fields
    is_corrected_on_site = db.Column(db.Boolean, nullable=True)
    is_repeat = db.Column(db.Boolean, nullable=True)

    # FK
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.inspection_id'))

    cols = ['violation_id', 'is_critical', 'code', 'description', 'comments', 'is_corrected_on_site', 'is_repeat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return('Violation {}'.format(self))

    def to_dict(self):
        data = {
            'violation_id': self.violation_id,
            'is_critical': self.is_critical,
            'code': self.code,
            'description': self.description,
            'comments': self.comments
        }
        if self.is_corrected_on_site not in ['', None]:
            data['is_corrected_on_site'] = self.is_corrected_on_site
        if self.is_repeat not in ['', None]:
            data['is_repeat'] = self.is_repeat
        return data

    def from_dict(self, data):
        for col in self.cols:
            if col in data:
                setattr(self, col, data[col])
