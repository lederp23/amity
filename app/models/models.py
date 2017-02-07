"""Database Models class module"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///app/database/amity.db")

class PersonModel(Base):
    """Model for Person"""
    __tablename__ = 'persons'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    position = Column (String(50))
    accomodate = Column (String(1))
    dateAdded = Column (DateTime())
    username = Column (String(50))

class FellowModel(Base):
    """Model for Fellow"""
    __tablename__ = 'fellows'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    dateAdded = Column (DateTime())
    username = Column (String(50))

class StaffModel(Base):
    """Model for Staff"""
    __tablename__ = 'staff'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    dateAdded = Column (DateTime())
    username = Column (String(50))

class AmityModel(Base):
    """Model for Amity"""
    __tablename__ = 'amity'
    id = Column(Integer, primary_key = True, autoincrement = True)
    rooms = Column(Integer)
    offices = Column(Integer)
    livingspace = Column(Integer)

class RoomModel(Base):
    """Model for Amity"""
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key = True, autoincrement = True)
    room_name = Column(String(50))
    room_type = Column(String(50))
    maximum_capacity = Column(Integer)
    space = Column(Integer)
    occuppants = Column(String(100))

Base.metadata.create_all(engine)
