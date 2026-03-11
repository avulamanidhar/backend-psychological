import datetime
from django.utils import timezone

def format_relative_time(timestamp_millis):
    """
    Python equivalent of TimeFormatUtils.java formatRelative.
    Takes epoch milliseconds and returns a human-readable string:
    'Today, h:mm a'
    'Yesterday, h:mm a'
    'MMM d, h:mm a'
    """
    dt = datetime.datetime.fromtimestamp(timestamp_millis / 1000.0, tz=timezone.get_current_timezone())
    now = timezone.localtime(timezone.now())
    
    time_str = dt.strftime("%I:%M %p").lstrip('0').lower() # e.g. "9:00 am"
    # Format to match Java's "h:mm a" exactly if needed, but python 'am/pm' is lowercase by default for %p in some locales.
    # Let's uppercase it just to be identical to java AM/PM
    time_str = dt.strftime("%I:%M %p").lstrip('0') 
    
    if now.date() == dt.date():
        return f"Today, {time_str}"
    elif (now.date() - datetime.timedelta(days=1)) == dt.date():
        return f"Yesterday, {time_str}"
    else:
        # e.g. "Oct 1, 9:00 AM" (MMM d)
        month_day = dt.strftime("%b %d").replace(" 0", " ") # Strip leading zero from day
        return f"{month_day}, {time_str}"
