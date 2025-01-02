import csv

## Getitng Data from csv

# Getting depot data
file_name1 = "depot.csv"
values_depot = []
with open(file_name1, "r", encoding="utf-8-sig") as depot_data:
    depot_reader = csv.DictReader(depot_data)

    for row in depot_reader:
        depot_id = row.get("DEPOT_ID")
        depot_name = row.get("DEPOT_NAME")
        values_depot.append((depot_id, depot_name))

# Getting vehicle type data
file_name2 = "vehicle_type.csv"
values_vehiType = []
with open(file_name2, "r", encoding="utf-8-sig") as vehiType_data:
    vehiType_reader = csv.DictReader(vehiType_data)

    for row in vehiType_reader:
        vehicle_type_id = row.get("VEHICLE_TYPE_ID")
        vehicle_type_name = row.get("VEHICLE_TYPE_NAME")
        values_vehiType.append((vehicle_type_id,vehicle_type_name))

# Getting company data
file_name4 = "company.csv"
values_company = []
with open(file_name4, "r", encoding="utf-8-sig") as company_data:
    company_reader = csv.DictReader(company_data)

    for row in company_reader:
        company_id = row.get("COMPANY_ID")
        company_name = row.get("COMPANY_NAME")
        values_company.append((company_id,company_name))


#
#
#
# Connecting database
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vshare_online",
    auth_plugin='mysql_native_password'
)
#
#
#


# 1 Depot
# Load DEPOT data into database
mycursor = mydb.cursor()
for value in values_depot:
    sql = "INSERT INTO DEPOT (DEPOT_ID,DEPOT_NAME)"
    sql += " VALUES(%s, %s)"
    val = value
    mycursor.execute(sql, val)

mydb.commit()
print("Depot data inserted!")
#
#

# 2 Vehicle type
# Load VEHICLE TYPE data into database
mycursor = mydb.cursor()
for value in values_vehiType:
    sql = "INSERT INTO vehicle_type (VEHICLE_TYPE_ID,VEHICLE_TYPE_NAME)"
    sql += " VALUES(%s, %s)"
    val = value
    mycursor.execute(sql, val)

mydb.commit()
print("\nVehicle Type data inserted!")
#
#

# 3 VEHICLE
# Loading Vehicle data into database
# Getting vehicle_Type_ID from database
vehicle_type_data = {}
def initVehicleTypeID():
    mycursor=mydb.cursor()
    sql="Select * from vehicle_type"
    mycursor.execute(sql)
    for d in mycursor:
        vehicle_type_id = d[0]
        vehicle_type_name = d[1]
        vehicle_type_data[vehicle_type_name]=vehicle_type_id

initVehicleTypeID()
def getVehicleTypeID(vehicle_type_name):
    return vehicle_type_data[vehicle_type_name]

# Getting Depot_ID from database
depot_data = {}
def initDepotID():
    mycursor=mydb.cursor()
    sql="Select * from depot"
    mycursor.execute(sql)
    for d in mycursor:
        depot_id = d[0]
        depot_name = d[1]
        depot_data[depot_name]=depot_id

initDepotID()
def getDepotID(depot_name):
    return depot_data[depot_name]

# Load Vehicle data into database
file_name3 = "VShareTesters.csv"
values_vehicle = []
with open(file_name3, "r", encoding="utf-8-sig") as vehicle_data:
    vehicle_reader = csv.DictReader(vehicle_data)

    for row in vehicle_reader:
        vrn = row.get("VRN")
        vehicle_type_name = row.get("Type")
        vehicle_type_id = getVehicleTypeID(vehicle_type_name)
        depot_name = row.get("Depot")
        depot_id = getDepotID(depot_name)
        # print("{0} {1} {2}".format(vrn, vehicle_type_id, depot_id))
        values_vehicle.append((vrn, vehicle_type_id, depot_id))

mycursor=mydb.cursor()
for value in values_vehicle:
    sql = "INSERT INTO VEHICLE (VRN,VEHICLE_TYPE_ID,DEPOT_ID)"
    sql += " VALUES(%s, %s, %s)"
    val = value
    mycursor.execute(sql, val)

mydb.commit()
print("\nVehicle data inserted!")
#
#

# 4 DRIVER
# # Loading Driver data into database
# Getting Vehicle_ID from database
vehicle_data = {}
def initVehicleID():
    mycursor=mydb.cursor()
    sql="Select * from vehicle"
    mycursor.execute(sql)
    for d in mycursor:
        vehicle_id = d[0]
        vrn = d[1]
        vehicle_data[vrn]=vehicle_id

initVehicleID()
def getVehicleID(vrn):
     return vehicle_data[vrn]

# Load Driver data into database
file_name4 = "VShareTesters.csv"
values_driver = []
with open(file_name4, "r", encoding="utf-8-sig") as driver_data:
    driver_reader = csv.DictReader(driver_data)

    for row in driver_reader:
        vrn = row.get("VRN")
        vehicle_id = getVehicleID(vrn)
        driver_name = row.get("Driver name")
        driver_mobile = row.get("Driver Mobile")
        driver_email = row.get("Driver Email")
        Login = row.get("Login hashed password")
        #print("{0} {1} {2} {3} {4}".format(vehicle_id, driver_name, driver_mobile, driver_email, Login))
        values_driver.append((driver_name, driver_mobile, driver_email, Login, vehicle_id))

mycursor=mydb.cursor()
for value in values_driver:
    sql = "INSERT INTO driver (DRIVER_NAME,DRIVER_MOBILE,DRIVER_EMAIL,LOGIN_HASHED_PASSWORD,VEHICLE_ID)"
    sql += " VALUES(%s, %s, %s, %s, %s)"
    val = value
    mycursor.execute(sql, val)

mydb.commit()
print("\nDriver data inserted!")
#
#


# 5 Company
# Load COMPANY data into database
mycursor = mydb.cursor()
for value in values_company:
    sql = "INSERT INTO COMPANY (COMPANY_ID,COMPANY_NAME)"
    sql += " VALUES(%s, %s)"
    val = value
    mycursor.execute(sql, val)

mydb.commit()
print("\nCompany data inserted!")
#
#

# # 6 Assign (Bridge)
# # Loading Usage data into database
# Getting Driver_Email from database
driver_data = {}
def initVehiIDFromD():
    mycursor=mydb.cursor()
    sql="Select * from driver"
    mycursor.execute(sql)
    for d in mycursor:
        driver_email = d[3]
        vehicle_id = d[5]
        driver_data[driver_email]=vehicle_id

initVehiIDFromD()
def getVehiIDFromD(driver_email):
     return driver_data[driver_email]

# getting all the possible companies name out
# Getting Company_ID from database
company_data = {}
def initCompanyID():
    mycursor=mydb.cursor()
    sql="Select * from company"
    mycursor.execute(sql)
    for d in mycursor:
        company_id = d[0]
        company_name = d[1]
        company_data[company_name]=company_id

companies = company_data.keys()

file_name7 = "VShareTesters.csv"
drivers = []
with open(file_name7,"r",encoding="utf-8-sig") as assign_data:
    assign_reader = csv.DictReader(assign_data)
    for row in assign_reader:
        #save the driver in memory for processing later
        drivers.append(row)
        # print(row)

values_assign =[]
#process one company at a time
for company in companies:
    #check if that driver is attached to that company
    for driver in drivers:
        assigned = driver.get(company)
        if(assigned == "TRUE"):
            driver_email = driver.get("Driver Email")
            vehicle_id = getVehiIDFromD(driver_email)
            company_id = getCompanyID(company)
            values_assign.append((vehicle_id,company_id))


mycursor = mydb.cursor()
for value in values_assign:
    sql = "INSERT INTO ASSIGN (VEHICLE_ID,COMPANY_ID)"
    sql += " VALUES(%s, %s)"
    val = value
    mycursor.execute(sql, val)

mydb.commit()
print("\nAssign data inserted!")
#
#

