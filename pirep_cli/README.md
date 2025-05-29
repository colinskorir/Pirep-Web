# PIREP CLI

A Python CLI tool for aviation professionals to create and manage Pilot Reports (PIREPs) using a SQLite database and SQLAlchemy ORM. Designed for Phase 3 CLI/ORM project requirements.

## Features
- Prompt-based CLI for entering and validating PIREP data
- Stores PIREPs in a SQLite database (`database.db`) with three related tables (Pirep, WeatherPhenomenon, Airport)
- Query and display all saved PIREPs with `--list` flag
- Strict input validation (ICAO, time, altitude, etc.)
- Modular, well-documented code using Python best practices
- Pipenv-managed environment for reproducibility

## Project Structure
```
pirep-cli/
├── pirep_cli/
│   ├── __init__.py       # Package marker
│   ├── cli.py            # CLI entry point
│   ├── models.py         # ORM models & input helpers
│   └── db_ops.py         # Database operations
├── Pipfile               # Pipenv config
├── Pipfile.lock          # Pipenv lock file
├── database.db           # SQLite database (auto-generated)
└── README.md             # This file
```

## Setup
1. **Install Pipenv:**
   ```bash
   pip install pipenv
   ```
2. **Install dependencies:**
   ```bash
   pipenv install
   ```
3. **Run the CLI:**
   ```bash
   pipenv run python -m pirep_cli.cli --save
   # or
   pipenv run python -m pirep_cli.cli --list
   ```

## Usage Example
```
$ pipenv run python -m pirep_cli.cli --save
PIREP Creator - Enter aviation weather report details
Report Type (UUA for Urgent, ROA for Routine): ROA
Location (4-letter ICAO code, e.g., KJFK): KATL
Airport Name (e.g., Hartsfield-Jackson Atlanta): Hartsfield-Jackson
Time of observation (HHMM UTC, e.g., 1430): 1200
Flight Level or Altitude (e.g., 050 for 5,000 ft, SFC for surface): 100
Aircraft Type (e.g., B737): A320
Enter observed weather phenomena (e.g., TURB, ICE, TS). Enter 'done' when finished.
Weather phenomenon (or 'done'): TURB
Weather phenomenon (or 'done'): done
Temperature (e.g., M05 for -5°C, P10 for +10°C, optional, press Enter to skip): M10
Wind (e.g., 270/15 for 270° at 15 knots, optional, press Enter to skip): 270/20
Remarks (optional, press Enter to skip): Moderate turbulence

Generated PIREP:
ROA PIREP KATL /TM 1200 /FL100 /TP A320 /WX TURB /TA M10 /WV 270/20 /RM Moderate turbulence
PIREP saved to database.db
```

## Database Schema
- **Airport**: id (PK), icao_code (unique), name
- **Pirep**: id (PK), report_type, airport_id (FK), time, altitude, aircraft_type, temperature, wind, remarks
- **WeatherPhenomenon**: id (PK), pirep_id (FK), phenomenon

## FAA PIREP Reference
- [FAA PIREP Guidelines](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap7_section_1.html)

## File Descriptions
- `pirep_cli/cli.py`: CLI entry point, argument parsing, main flow
- `pirep_cli/models.py`: ORM models, input/validation helpers
- `pirep_cli/db_ops.py`: Database save/query logic
- `Pipfile`: Pipenv config (Python 3.8+, SQLAlchemy)
- `README.md`: Project documentation

## Coding Best Practices
- Modular, single-responsibility functions
- Docstrings for all functions
- Error handling for input and database operations
- Uses lists (weather phenomena), dicts (PIREP data), tuples (validation/query results)
- No network calls; only SQLite file I/O

---

**PIREP CLI** is designed for educational use and demonstration of Python CLI, ORM, and data validation best practices.
