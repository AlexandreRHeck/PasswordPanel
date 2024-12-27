from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Clinic para representar uma clínica
class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)  # Localização opcional

# Modelo Password associado à clínica
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    guiche = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)  # Relaciona com a clínica
    clinic = db.relationship('Clinic', backref=db.backref('passwords', lazy=True))

# Modelo Attendant (Atendente) associado à clínica
class Attendant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)  # Relaciona com a clínica
    clinic = db.relationship('Clinic', backref=db.backref('attendants', lazy=True))
