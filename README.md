# iRacingRPMToolbox
Python toolbox for the iRacing championship RPM

## Setup your local development
This toolbox has some dependencies that need to be installed before you can run it.

It is recommended to create a virtual environment to isolate this project and its packages
from your system, but it is not required.

### Virtual environment
To create a venv:
`python3 -m venv ./venv`

To activate it:
`source venv/bin/activate`

See: https://docs.python.org/3/library/venv.html

### Installing dependencies
To install dependencies:
`pip install -r requirements.txt`

### Credentials
iRacing credentials are needed in order to login to the API.

Define the following environment variables:
`IRAPI_USR` for username
`IRAPI_PWD` for password

## Running instructions

### Computing the statistics for a race
To compute and export the json containing all the statistics for a race:
handle_results.py subsession_id output_file

subsession_id: Id of the race session.
output_file: Output file to be written.

### Extracting the laps with car contact
To extract all laps where a car contact occurred with the names of the drivers involved:
notes_incidents.py subsession_id output_file

subsession_id: Id of the race session.
output_file: Output file to be written.

### Plot race stats
`python src/generate_stats.py <subsession_id>`
