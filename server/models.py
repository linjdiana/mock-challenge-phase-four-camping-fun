from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-signups',
                       '-campers.activities', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),onupdate=db.func.now())

    signups = db.relationship('Signup', backref='activity')
    activities = association_proxy('signups', 'activity')

    def __repr__(self):
        return f'<Activity {self.name}, {self.difficulty}>'

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    # serialize_rules = ('-camper.signups',)
    # serialize_rules = ('-activity.signups',)
    serialize_rules = ('-camper.signups', '-activity.signups',
                       '-camper.activities', '-activity.campers', '-created_at', '-updated_at')

    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),onupdate=db.func.now())

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    @validates('time')
    def validate_time(self, key, time):
        if time > 23:
            raise ValueError('Time must be between 0 and 23')
        return time
    
    @validates('camper_id')
    def validates_camper_id(self, key, value):
        campers = Camper.query.all()
        camper_ids = [camper.id for camper in campers]
        if not value in camper_ids:
            raise ValueError("Not a camper.")
        return value

    @validates('activity_id')
    def validates_activity_id(self, key, value):
        activities = Activity.query.all()
        activity_ids = [activity.id for activity in activities]
        if not value in activity_ids:
            raise ValueError("Not an activity.")
        return value

    def __repr__(self):
        return f'<Signup {self.time}>'

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-signups', '-created_at',
                       '-updated_at', '-activities.created_at', '-activities.updated_at', '-activities.campers')

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(),onupdate=db.func.now())

    signups = db.relationship('Signup', backref='camper')
    activities = association_proxy('signups', 'activity')

    @validates('name')
    def validate_name(self, key, name):
         if name == '':
             raise ValueError('must have a name')
         return name

    @validates('age')
    def validate_age(self, key, age):
        if age < 8 or age > 18:
            raise ValueError('age must be between 8 and 18')
        return age 
    
    def __repr__(self):
        return f'<Camper {self.name}>'

    



