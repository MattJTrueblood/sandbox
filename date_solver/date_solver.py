import sys
from datetime import date, datetime, timedelta

# Note:  python dates work for any date between Jan 1, 1 AD and Dec 31, 9999 AD.

# finds the number of weekdays between two dates (inclusive)
def weekdays_between(first_date: date, second_date: date) -> int:
	# edge case:  if they are the same day
	if first_date == second_date:
		return 1 if weekday_of_gregorian_ordinal(to_gregorian_ordinal(first_date)) < 5 else 0

	start_date, end_date = sorted([first_date, second_date]) # dates could be in any order; now they are earlier and later.
	num_days_between_inclusive = days_between_inclusive(start_date, end_date)
	start_weekday = weekday_of_gregorian_ordinal(to_gregorian_ordinal(start_date)) # Monday=0, Sunday=6.  Therefore, < 5 means weekday

	# an interval can be considered as some full weeks plus some extra days
	num_full_weeks_between = num_days_between_inclusive // 7
	num_extra_days_between = num_days_between_inclusive % 7

	# start with weeks.  For each full week, we add 5 weekdays.
	num_weekdays = num_full_weeks_between * 5

	# depending on what weekday we started at, we need to figure out whether each extra day (max 6) is a weekday
	for i in range(num_extra_days_between):
		weekday_plus_i = (start_weekday + i) % 7
		if weekday_plus_i < 5:
			num_weekdays += 1

	return num_weekdays

# finds the number of days between two dates by using gregorian ordinals (day counter starting at 0001-01-01 = 1)
def days_between_inclusive(start_date: date, end_date: date) -> int:
	start_ordinal = to_gregorian_ordinal(start_date)
	end_ordinal = to_gregorian_ordinal(end_date)
	return end_ordinal - start_ordinal + 1

# manually calculates the gregorian ordinal of a given day
def to_gregorian_ordinal(some_date: date) -> int:
	days = gregorian_days_from_year(some_date.year)
	days += gregorian_days_from_month(some_date.year, some_date.month)
	days += some_date.day
	return days

# calculates the number of total days added to a gregorian ordinal from the year alone.
def gregorian_days_from_year(year: int) -> int:
	# leap years are every 4 years, skipping every 100 years, but not every 400 years.

	# first, every 400 year period should have the same number of days.
	num_400_years_blocks = (year - 1) // 400
	days = num_400_years_blocks * (400 * 365 + 100 - 3)

	# we can do the same for every 100 year period in the remainder
	remaining_years = (year - 1) % 400
	num_100_years_blocks = remaining_years // 100
	days += num_100_years_blocks * (100 * 365 + 25 - 1)

	# and once again, for every 4 year period in the remainder of the 100 years block
	remaining_years %= 100
	num_4_years_blocks = remaining_years // 4
	days += num_4_years_blocks * (4 * 365 + 1)

	# finally, the remaining 0-3 days can be checked individually
	remaining_years %= 4
	for i in range(1, remaining_years + 1):
		days += 366 if is_leap_year((year - 1) - remaining_years + i) else 365

	return days

# calculates whether a given year is a leap year or not
def is_leap_year(year):
	return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# calculates the number of total days added to the gregorian ordinal from the month alone.
def gregorian_days_from_month(year: int, month: int) -> int:
	days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if is_leap_year(year):
		days_in_months[1] = 29
	result = sum(days_in_months[:month-1])
	return result

# calculates the weekday without using python's built-in datetime.  Jan 1, 1 AD (in proleptic gregorian dates) is Monday.
# returns integer day of the week, starting with monday=0 (same as python's date.weekday() implementation)
def weekday_of_gregorian_ordinal(ordinal: int) -> int:
    days_since_jan_1_1_ad = ordinal - 1
    return (days_since_jan_1_1_ad % 7)

# parses a YYYY-MM-DD date string from command-line-input
def parse_date(date_str: str) -> date:
	try:
		return datetime.strptime(date_str, "%Y-%m-%d").date()
	except ValueError:
		print(f"Invalid date format: {date_str}. Please enter the date in YYYY-MM-DD format.")
		sys.exit(1)

# called when running this script directly
def main():
	if len(sys.argv) != 3:
		print("Usage: python date_solver.py <date1> <date2>")
		sys.exit(1)

	# parse each of the user-inputted date strings and pass them into the weekday solver function
	date_1 = parse_date(sys.argv[1])
	date_2 = parse_date(sys.argv[2])
	output = weekdays_between(date_1, date_2)

	# print output of weekdays_between function to user
	print("num weekdays between inputted dates (inclusive):", output)
	
def is_valid_date(year, month, day):
	try:
		date(year, month, day)
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	main()


#### TESTS ####

# test function to verify correctness of to_gregorian_ordinal function by checking it against python's implementation
def test_my_gregorian_ordinal():
	print("testing to_gregorian_ordinal...")
	start_date = date(1, 1, 1)  # start from Jan 1, 1 AD
	end_date = date(9999, 12, 31)  # end at Dec 31, 9999 AD

	current_date = start_date

	while True:
		my_ordinal = to_gregorian_ordinal(current_date)
		python_ordinal = current_date.toordinal()
        
		if my_ordinal != python_ordinal:
			print(f"Error on date {current_date}: my ordinal {my_ordinal}, python ordinal {python_ordinal}")
			return

		# check for end of loop
		if current_date == end_date:
			break

		# increment day by one
		current_date += timedelta(days=1)

	print("Test passed!")

# test function to verify correctness of days_between_inclusive function by checking it against datetime implementation
def test_days_between_inclusive():
	print("testing days_between...")

	# some date ranges to check
	test_dates = [
		(date(2023, 1, 1), date(2023, 1, 1)),   # same start and end date
		(date(2023, 1, 1), date(2023, 1, 2)),   # consecutive days
		(date(2023, 1, 1), date(2023, 1, 31)),  # same month
		(date(2023, 1, 1), date(2023, 12, 31)), # same year
		(date(2020, 1, 1), date(2021, 1, 1)),   # across leap year
		(date(1, 1, 1), date(9999, 12, 31)), # large range
	]

	for start_date, end_date in test_dates:
		my_days_between = days_between_inclusive(start_date, end_date)
		python_days_between = (end_date - start_date).days + 1
		if my_days_between != python_days_between:
			print(f"Error on days between {start_date} and {end_date}: my function {my_days_between}, python's {python_days_between}")
			return

	print("Test passed!")


#test_my_gregorian_ordinal()
#test_days_between_inclusive()