from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from database import Base
from datetime import datetime

class Donnee(Base):
    __tablename__ = 'donnee'
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    unite = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    capteurid = Column(Integer, ForeignKey('capteur.name'), nullable=False)

    def __init__(self, value=None, unite=None, date=None, capteur=None):
        self.value = value
        self.unite = unite
        self.date = date
        self.capteurid = capteur

    def date_str(self):
        return str(self.date)

    def __repr__(self):
        return '<Donnee id={} valeur={} unite={} date={} capteur={}>'.format(self.id, self.value, self.unite, self.date_str(), self.capteurid)

class Capteur(Base):
    __tablename__ = 'capteur'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Capteur id={} name={}>'.format(self.id, self.name)