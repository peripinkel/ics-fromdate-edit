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
    
    # Uses array to copy properties from the original
    calender_properties = ["method", "prodid", "version", "x-wr-calname"]
    for item in calender_properties:
        calendar.add(item, original_calendar.get(item))

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

        # Goes through array to copy event types
        # Note to self: ! Change this to read from the file in the future !
        event_properties = ["uid", "summary", "dtstart", "dtend", "class", "priority", "dtstamp", "transp", "status", "sequence", "location"]
        for item in event_properties:
            # This includes rough editing codes because my study has a lot of study additions, I will change the method in the future (hopefully)
            current_event = event.get(item)
            if item == "summary":
                if current_event[6:].startswith("SW1"):
                    if current_event[20:].startswith("SW1B"):
                        new_event.add(item, current_event[27:])
                    else:
                        new_event.add(item, current_event[30:])
                elif current_event[6:].startswith("EN"):
                    new_event.add(item, current_event[14:])
                else:
                    new_event.add(item, current_event)
            else:
                new_event.add(item, current_event)
        
        new_calendar.add_component(new_event)


create = open('example.ics', 'wb')
create.write(new_calendar.to_ical())
create.close()