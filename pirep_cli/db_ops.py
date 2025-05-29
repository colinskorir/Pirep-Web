"""
db_ops.py: Database operations for saving and querying PIREPs using SQLAlchemy ORM.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models import Base, Pirep, WeatherPhenomenon, Airport, format_pirep
except ImportError as import_err:
    raise ImportError(f"Import error in db_ops.py: {import_err}. Make sure all dependencies are installed and you are running from the project root.") from import_err

DB_URL = 'sqlite:///database.db'
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def save_pirep(data):
    """Save a PIREP and related data to the database."""
    session = Session()
    try:
        airport = session.query(Airport).filter_by(icao_code=data['icao_code']).first()
        if not airport:
            airport = Airport(icao_code=data['icao_code'], name=data['airport_name'])
            session.add(airport)
            session.flush()  # Assigns airport.id
        pirep = Pirep(
            report_type=data['report_type'],
            airport_id=airport.id,
            time=data['time'],
            altitude=data['altitude'],
            aircraft_type=data['aircraft_type'],
            temperature=data.get('temperature'),
            wind=data.get('wind'),
            remarks=data.get('remarks')
        )
        session.add(pirep)
        session.flush()  # Assigns pirep.id
        for wx in data['weather_phenomena']:
            session.add(WeatherPhenomenon(pirep_id=pirep.id, phenomenon=wx))
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def list_pireps():
    """Query all PIREPs and return formatted strings."""
    session = Session()
    try:
        pireps = session.query(Pirep).all()
        result = []
        for pirep in pireps:
            airport = pirep.airport
            wx_list = [wx.phenomenon for wx in pirep.weather_phenomena]
            data = {
                'report_type': pirep.report_type,
                'icao_code': airport.icao_code,
                'airport_name': airport.name,
                'time': pirep.time,
                'altitude': pirep.altitude,
                'aircraft_type': pirep.aircraft_type,
                'weather_phenomena': wx_list,
                'temperature': pirep.temperature,
                'wind': pirep.wind,
                'remarks': pirep.remarks
            }
            result.append(format_pirep(data))
        return result
    finally:
        session.close()
