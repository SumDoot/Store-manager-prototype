import datetime
import urllib3

url = "http://192.168.31.43:8085/StoreAPI.php"


# function to convert date to a desireable format
def parseDate(date, isStart):
    try:
        if isStart:
            return str(datetime.datetime.strptime(date + " 00:00", '%d.%m.%Y %H:%M')).replace(" ", "T")
        else:
            return str(datetime.datetime.strptime(date + " 23:59", '%d.%m.%Y %H:%M')).replace(" ", "T")
    except ValueError:
        print("Invalid format! Please try again!")
        return parseDate(input("Input date (format DD.MM.YYYY): "), isStart)


# function to get data from API
def useAPI(RequestType, FullURL):
    return urllib3.PoolManager().request(RequestType, FullURL).data.decode("utf-8")


# function for showing income / spendings / total
def showTotal(startDate, endDate):
    print(f"Data from {startDate} to {endDate}")


# function for adding purchases
def addSalesEntry():
    while True:
        print("adding sales entry...")
        if input("add another? leave empty continue: ") != "":
            break


# function to provide functionality for privilidged users
def FullAccess():
    while True:
        match input("""
Please enter number of option to continue: 
0 - show income, spendings and total in a time period
1 - add new sales entry
2 - add new restock entry
leave blank to exit

"""):
            case "":
                break
            
            case "0":
                showTotal(parseDate(input("Input start date (format DD.MM.YYYY): "), True), parseDate(input("Input end date(format DD.MM.YYYY): "), False))

            case "1":
                addSalesEntry()

            case "2":
                print("doing no munei ad produc...")

            case _:
                print("This is not a defined function! Please try again.")


# ----- MAIN CODE -----


# authenticate user
while True:
    username = input("Enter username: ")
    password = input("Enter password: ")
    userRole = useAPI("GET", url + f"?user={username}&pass={password}&purp=a")

    match userRole:
        case "Pardevejs":
            break
        case "Ipasnieks":
            break
        case _:
            print(userRole)

print(f"Hello, {userRole}!")


# give user appropriate access
match userRole:
    case "Pardevejs":
        addSalesEntry()
    case "Ipasnieks":
        FullAccess()

print("Exiting...")