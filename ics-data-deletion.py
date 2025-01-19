import icalendar
from icalendar import Calendar, Event
import pytz
from datetime import datetime
from datetime import date
from pathlib import Path

# Set the path
calendar_path = Path("src/icalendar/school-schedule.ics")

# Load the ics file into the script
def load_file(ics_path: Path):
    with ics_path.open() as file:
        return icalendar.Calendar.from_ical(file.read())

loaded_calendar = load_file(calendar_path)

# Get the time in the Y-m-d H-M-Sz
def current_time_formatted():
    # Set the timezone and get the time
    timezone = pytz.timezone("Europe/Amsterdam")
    current_datetime = datetime.now(timezone)
    current_datetime = current_datetime.replace(microsecond=0)
    current_date = current_datetime.date()

    return current_date

# Makes sure the dtstart is always in date format
def dtstart_date_check(dtstart):
    if isinstance(dtstart, datetime):
        dtstart_checkable = dtstart.date()
    else:
        dtstart_checkable = dtstart
    return dtstart_checkable

# Inititiates calendar with properties of the original
def initiate_calendar(original_calendar: Calendar):
    calendar = Calendar()
    calendar.add('method', original_calendar.get('METHOD'))
    calendar.add('prodid', original_calendar.get('PRODID'))
    calendar.add('version', original_calendar.get('VERSION'))
    calendar.add('x-wr-calname', original_calendar.get('X-WR-CALNAME'))

    return calendar

# Initiate new calendar
new_calendar = initiate_calendar(loaded_calendar)

# Go through file and parse only certain dates
today = current_time_formatted()
for event in loaded_calendar.walk('VEVENT'):
    dtstart = event.get("DTSTART").dt
    dtstart_date = dtstart_date_check(dtstart)
    if dtstart_date >= today:
        # Create events needed for the new calendar file
        new_event = Event()
        new_event.add('uid', event.get('UID'))
        new_event.add('summary', event.get('SUMMARY'))
        new_event.add('dtstart', event.get('DTSTART'))
        new_event.add('dtend', event.get('DTEND'))
        new_event.add('class', event.get('CLASS'))
        new_event.add('priority', event.get('PRIORITY'))
        new_event.add('dtstamp', event.get('DTSTAMP'))
        new_event.add('transp', event.get('TRANSP'))
        new_event.add('status', event.get('STATUS'))
        new_event.add('sequence', event.get('SEQUENCE'))
        new_calendar.add_component(new_event)


create = open('example.ics', 'wb')
create.write(new_calendar.to_ical())
create.close()