from datetime import datetime

def get_days_from_today(date):

    # Get the current date
    current_date = datetime.now()

    # Get the date from the argument
    date = datetime.strptime(date, '%Y-%m-%d')

    # Calculate the difference between the two dates
    difference = current_date - date

    # Return the difference in days
    return difference.days


print(get_days_from_today('2025-10-09'))