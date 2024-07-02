import sys
from datetime import date, datetime

# Note:  python dates work for any date between Jan 1, 1 AD and Dec 31, 9999 AD.

# finds the number of weekdays between two dates (inclusive)
def weekdays_between(first_date: date, second_date: date) -> int:
	# edge case:  if they are the same day
	if first_date == second_date:
		return 1 if first_date.weekday() < 5 else 0

	start_date, end_date = sorted([first_date, second_date]) # dates could be in any order; now they are earlier and later.
	start_weekday = start_date.weekday() # Monday=0, Sunday=6.  Therefore, < 5 means weekday
	num_days_between_inclusive = days_between_inclusive(start_date, end_date)

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

# manually calculates the days between two dates by using gregorian ordinals (day counter starting at 0001-01-01 = 1)
def days_between_inclusive(start_date: date, end_date: date) -> int:
	start_ordinal = start_date.toordinal()
	end_ordinal = end_date.toordinal()
	return end_ordinal - start_ordinal + 1

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
	
if __name__ == "__main__":
	main()