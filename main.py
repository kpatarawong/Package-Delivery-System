# Kalvin Patarawong
# Student ID:009931191
# C950 WGUPS ROUTING PROGRAM

import csv
import datetime
from hashtable import HashTable
from package import Packages
from truck import Trucks

# Load the CSV files
with open("CSV/addressCSV.csv") as addyCSV:
    AddressCSV = csv.reader(addyCSV)
    AddressCSV = list(AddressCSV)

with open("CSV/distanceCSV.csv") as disCSV:
    DistanceCSV = csv.reader(disCSV)
    DistanceCSV = list(DistanceCSV)

with open("CSV/packageCSV.csv") as packCSV:
    PackageCSV = csv.reader(packCSV)
    PackageCSV = list(PackageCSV)

# Hash table for the packages
packageHash = HashTable()

# Load package data into the hash table
def loadPackageData(filename):
    with open(filename) as packageInfo:
        packageData = csv.reader(packageInfo, delimiter=',')
        next(packageData)  # Skip header row
        for package in packageData:
            pID = int(package[0])
            pStreet = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At the Hub"

            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)

            # Insert Package object into HashTable
            packageHash.insert(pID, p)


# Load distance data between two locations
def loadDistanceData(x_value, y_value):
    distance = DistanceCSV[x_value][y_value]
    if distance == '':
        distance = DistanceCSV[y_value][x_value]
    return float(distance)

# Load address data for matching delivery location
def loadAddressData(address):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])
    return None


# Nearest neighbor algorithm to deliver the packages on truck
def truckDeliverPackages(truck):
    # List for all packages that needs to be delivered
    enroute = []
    # Put packages from the hash table into list
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        if package:  # Only add if package is found
            enroute.append(package)

    truck.packages.clear()

    # While there are packages left to be delivered, the algorithm will run
    while len(enroute) > 0:
        nextAddy = float('inf')  # Set an initial very high value
        nextPackage = None

        for package in enroute:
            address_id = loadAddressData(package.street)
            if address_id is None:
                continue

            distance = loadDistanceData(loadAddressData(truck.currentLocation), address_id)
            if distance <= nextAddy:
                nextAddy = distance
                nextPackage = package

        if nextPackage:
            truck.packages.append(nextPackage.ID)
            enroute.remove(nextPackage)
            truck.miles += nextAddy
            truck.currentLocation = nextPackage.street
            truck.time += datetime.timedelta(hours=nextAddy / 18)  # Time = distance / speed (converted to hours)
            nextPackage.deliveryTime = truck.time
            nextPackage.departureTime = truck.departTime

# Load package CSV data and deliver packages
loadPackageData('CSV/packageCSV.csv')

# Manually load truck and assign packages to departure time
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39])

# Put trucks through loading process
truckDeliverPackages(truck1)
truckDeliverPackages(truck2)
# The below line of code ensures that truck 3 does not leave until first two trucks finish delivering packages
truck3.departTime = min(truck1.time, truck2.time)
truckDeliverPackages(truck3)

# Print title
print("Western Governors University Parcel Service (WGUPS)")

#User Interface
def show_menu():
    print("\n***************************************")
    print("1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status with a Time")
    print("4. Exit the Program")
    print("***************************************")

# Print all status and total mileage
def print_all_status_and_total_mileage(trucks, packageHash):
    total_miles = sum(truck.miles for truck in trucks)
    print(f"\nTotal mileage for all trucks: {total_miles:.2f} miles")
    for bucket in packageHash.table:
        for key, package in bucket:
            print(package)

# Print single package status with time
def get_single_package_status(packageHash, time_change):
    package_id = int(input("Enter Package ID: "))
    package = packageHash.search(package_id)
    if package:
        package.statusUpdate(time_change)
        print(package)
    else:
        print("Package ID not found.")

# Print all package status with time
def get_all_package_status(packageHash, time_change):
    for bucket in packageHash.table:
        for key, package in bucket:
            package.statusUpdate(time_change)
            print(package)

# Choices for user input
def main(trucks, packageHash):
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            print_all_status_and_total_mileage(trucks, packageHash)
        elif choice == '2':
            user_time = input("Enter a time (HH:MM): ")
            hours, minutes = map(int, user_time.split(":"))
            time_change = datetime.timedelta(hours=hours, minutes=minutes)
            get_single_package_status(packageHash, time_change)
        elif choice == '3':
            user_time = input("Enter a time (HH:MM): ")
            hours, minutes = map(int, user_time.split(":"))
            time_change = datetime.timedelta(hours=hours, minutes=minutes)
            get_all_package_status(packageHash, time_change)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

# Run the main program
main([truck1, truck2, truck3], packageHash)