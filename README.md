USE

  python -m pirep_cli.main --save
    <!-- This is to save the pirep data to the database. -->



  python -m pirep_cli.main --list
    <!-- This is to list the pirep data from the database. -->


Use any airport in the world and you will get the pirep data for that airport.


This project is a command-line tool for retrieving and managing PIREP (Pilot Reports) data for any airport worldwide. It allows users to save PIREP data to a database and list stored PIREP reports using simple commands.

Here’s an example of what the terminal output might look like when listing PIREP data:

$ python -m pirep_cli.main --list

PIREP Reports for KJFK:
-----------------------
Time: 2025-05-29 14:32
Type: Turbulence
Details: Moderate turbulence reported at 10,000 ft.

Time: 2025-05-29 13:15
Type: Icing
Details: Light icing encountered during descent.