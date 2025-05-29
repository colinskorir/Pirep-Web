"""
models.py: Defines SQLAlchemy ORM models and input/validation helpers for PIREP CLI.
"""
import re
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Airport(Base):
    """ORM model for Airport table."""
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    icao_code = Column(String(4), unique=True, nullable=False)
    name = Column(String(64), nullable=False)
    pireps = relationship('Pirep', back_populates='airport')

class Pirep(Base):
    """ORM model for PIREP table."""
    __tablename__ = 'pirep'
    id = Column(Integer, primary_key=True)
    report_type = Column(String(3), nullable=False)
    airport_id = Column(Integer, ForeignKey('airport.id'), nullable=False)
    time = Column(String(4), nullable=False)
    altitude = Column(String(6), nullable=False)
    aircraft_type = Column(String(16), nullable=False)
    temperature = Column(String(6))
    wind = Column(String(16))
    remarks = Column(String(128))
    weather_phenomena = relationship('WeatherPhenomenon', back_populates='pirep', cascade="all, delete-orphan")
    airport = relationship('Airport', back_populates='pireps')

class WeatherPhenomenon(Base):
    """ORM model for WeatherPhenomenon table."""
    __tablename__ = 'weather_phenomenon'
    id = Column(Integer, primary_key=True)
    pirep_id = Column(Integer, ForeignKey('pirep.id'), nullable=False)
    phenomenon = Column(String(32), nullable=False)
    pirep = relationship('Pirep', back_populates='weather_phenomena')

def validate_icao(icao):
    """Validate ICAO code: must be 4 uppercase letters."""
    return bool(re.fullmatch(r'[A-Z]{4}', icao))

def validate_time(timestr):
    """Validate time: must be HHMM (24-hour UTC)."""
    if not re.fullmatch(r'\d{4}', timestr):
        return False
    try:
        datetime.strptime(timestr, '%H%M')
        return True
    except ValueError:
        return False

def validate_altitude(alt):
    """Validate altitude: 3 digits (e.g., 050) or SFC."""
    return bool(re.fullmatch(r'(SFC|\d{3})', alt))

def get_pirep_data():
    """Prompt user for PIREP data, validate, and return as dict."""
    data = {}
    # Report type
    while True:
        rt = input("Report Type (UUA for Urgent, ROA for Routine): ").strip().upper()
        if rt in ("UUA", "ROA"):
            data['report_type'] = rt
            break
        print("Invalid report type. Enter 'UUA' or 'ROA'.")
    # ICAO code
    while True:
        icao = input("Location (4-letter ICAO code, e.g., KJFK): ").strip().upper()
        if validate_icao(icao):
            data['icao_code'] = icao
            break
        print("Invalid ICAO code. Must be 4 letters (e.g., KJFK).")
    # Airport name
    while True:
        name = input("Airport Name (e.g., Hartsfield-Jackson Atlanta): ").strip()
        if name:
            data['airport_name'] = name
            break
        print("Airport name cannot be empty.")
    # Time
    while True:
        tm = input("Time of observation (HHMM UTC, e.g., 1430): ").strip()
        if validate_time(tm):
            data['time'] = tm
            break
        print("Invalid time. Must be HHMM (e.g., 1430).")
    # Altitude
    while True:
        alt = input("Flight Level or Altitude (e.g., 050 for 5,000 ft, SFC for surface): ").strip().upper()
        if validate_altitude(alt):
            data['altitude'] = alt
            break
        print("Invalid altitude. Must be 3 digits (e.g., 050) or SFC.")
    # Aircraft type
    while True:
        tp = input("Aircraft Type (e.g., B737): ").strip().upper()
        if tp:
            data['aircraft_type'] = tp
            break
        print("Aircraft type cannot be empty.")
    # Weather phenomena (list)
    phenomena = []
    print("Enter observed weather phenomena (e.g., TURB, ICE, TS). Enter 'done' when finished.")
    while True:
        wx = input("Weather phenomenon (or 'done'): ").strip().upper()
        if wx == 'DONE':
            break
        if wx:
            phenomena.append(wx)
    if not phenomena:
        print("At least one weather phenomenon is required.")
        return get_pirep_data()
    data['weather_phenomena'] = phenomena
    # Optional fields
    temp = input("Temperature (e.g., M05 for -5°C, P10 for +10°C, optional, press Enter to skip): ").strip().upper()
    data['temperature'] = temp if temp else None
    wind = input("Wind (e.g., 270/15 for 270° at 15 knots, optional, press Enter to skip): ").strip().upper()
    data['wind'] = wind if wind else None
    remarks = input("Remarks (optional, press Enter to skip): ").strip()
    data['remarks'] = remarks if remarks else None
    return data

def format_pirep(data):
    """Format PIREP dict as a string per FAA standards."""
    parts = [
        f"{data['report_type']} PIREP {data['icao_code']}",
        f"/TM {data['time']}",
        f"/FL{data['altitude']}",
        f"/TP {data['aircraft_type']}",
        f"/WX {' '.join(data['weather_phenomena'])}"
    ]
    if data.get('temperature'):
        parts.append(f"/TA {data['temperature']}")
    if data.get('wind'):
        parts.append(f"/WV {data['wind']}")
    if data.get('remarks'):
        parts.append(f"/RM {data['remarks']}")
    return ' '.join(parts)
