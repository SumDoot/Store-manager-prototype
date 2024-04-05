import datetime

# function for selecting action
def mainSelection(): 
    return input("""
Please enter number of option to continue: 
0 - show income, spendings and total in a time period
1 - add new sales entry
2 - add new spendings entry
leave blank to exit

""")

# function to convert date to a desireable format
def parseDate(date, isStart):
    try:
        if isStart:
            return datetime.datetime.strptime(date + " 00:00", '%d.%m.%Y %H:%M')
        else:
            return datetime.datetime.strptime(date + " 23:59", '%d.%m.%Y %H:%M')
    except ValueError:
        print("Invalid format! Please try again!")
        return parseDate(input("Input date (format DD.MM.YYYY): "), isStart)

# function for showing income / spendings / total
def showTotal(startDate, endDate):
    print(f"doing number show from {startDate} to {endDate}")


# main script
while True:
    match mainSelection():
        case "":
            break
        
        case "0":
            showTotal(parseDate(input("Input start date (format DD.MM.YYYY): "), True), parseDate(input("Input end date(format DD.MM.YYYY): "), False))

        case "1":
            print("doing add munei row...")

        case "2":
            print("doing add no munei row...")

        case _:
            print("This is not a defined function! Please try again.")

print("Exiting...")