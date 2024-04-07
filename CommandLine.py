import datetime
import urllib3
from getpass import getpass

url = "php-api-url-here"


# function to get a date from user
def GetDate():
    try:
        endDate = input("Input end date (format DD.MM.YYYY) or today (t): ")
        if endDate == "t":
            endDate = datetime.date.today()
        else:
            endDate = datetime.datetime.strptime(endDate + " 23:59", '%d.%m.%Y %H:%M')

        print("Input start date (format DD.MM.YYYY) or period")
        startDate = input("(t - today, d - day, w - week, m - month, y - year): ")
        match startDate:
            case "t":
                startDate = datetime.date.today().strftime("%d.%m.%Y")
            case "d":
                startDate = endDate.strftime("%d.%m.%Y")
            case "w":
                startDate = endDate - datetime.timedelta(days=7)
                startDate = startDate.strftime("%d.%m.%Y")
            case "m":
                startDate = endDate - datetime.timedelta(days=30)
                startDate = startDate.strftime("%d.%m.%Y")
            case "y":
                startDate = endDate - datetime.timedelta(days=365)
                startDate = startDate.strftime("%d.%m.%Y")

        endDate = str(datetime.datetime.strptime(endDate.strftime("%d.%m.%Y") + " 23:59", '%d.%m.%Y %H:%M')).replace(" ", "T")
        startDate = str(datetime.datetime.strptime(startDate + " 00:00", '%d.%m.%Y %H:%M')).replace(" ", "T")
        return startDate + ","+ endDate

    except ValueError:
        print("Invalid format! Please try again!")
        return GetDate()


# function to get data from API
def useAPI(RequestType, tagsOnlyURL):
    return urllib3.PoolManager().request(RequestType, url + tagsOnlyURL).data.decode("utf-8")


# function for showing income / spendings / total
def showTotal():
    Dates = GetDate().split(",")

    print(f"Data from {Dates[0]} to {Dates[1]}")
    totals = useAPI("GET", f"?user={username}&pass={password}&purp=g&starttime={Dates[0]}&endtime={Dates[1]}").split(",")
    print(f"Profit: {totals[0]}€, Loss: {totals[1]}€, Total: {totals[2]}€")


# function for adding purchases
def addSalesEntry():
    while True:
        itemCodes = []
        itemCounts = []
        while True:
            itemCodes.append(input("Enter item code: "))
            itemCounts.append(input("Enter item count: "))
            if input("Add another PRODUCT? Leave empty to add another, anyting else to exit: ") != "":
                break
        allItems = ""
        for x in range(len(itemCodes)):
            allItems += itemCodes[x] + "x" + itemCounts[x] + ","
        print(f'Transaction total: {useAPI("GET", f"?user={username}&pass={password}&purp=s&items={allItems}")} €')
        if input("Create another PURCHASE? Leave empty to create, anyting else to exit: ") != "":
            break


# function for adding restocks
def addRestockEntry():
    while True:
        itemCode = input("Enter item code: ")
        itemCount = input("Enter item count: ")
        itemPrice = input("Enter item price (format as 123.45): ")
        useAPI("GET", f"?user={username}&pass={password}&purp=r&item={itemCode}&count={itemCount}&price={itemPrice}")
        print("Added restocking entry.")
        if input("Add another? Leave empty to add, anyting else to exit: ") != "":
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
                showTotal()
            case "1":
                addSalesEntry()
            case "2":
                addRestockEntry()
            case _:
                print("This is not a defined function! Please try again.")


# -----------------------------------------
# --------------- MAIN CODE ---------------
# -----------------------------------------


# authenticate user
while True:
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    userRole = useAPI("GET", f"?user={username}&pass={password}&purp=a")

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
