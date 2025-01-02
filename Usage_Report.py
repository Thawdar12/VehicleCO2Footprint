import mysql.connector

print("Welcome!")

print("\n~~~~ MENU ~~~~")
print("\n1. Show Vehicle Usage Data (format 1) \n2. Show Vehicle Usage Data (format 2) "
      "\n3. Exit")
option = int(input("Enter your option ==> "))

while option == 1 or option == 2:

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vshare_online_usage",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()
    star = "*****************************"

    if option == 1:
        # Format 1
        sql1 = ("SELECT SUM(Distance) As Total_Distance, VEHICLE_TYPE_ID, VEHICLE_TYPE_NAME,company_type "
               " FROM ( SELECT V.VEHICLE_ID, VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, VU.DISTANCE, C.COMPANY_NAME, C.COMPANY_TYPE "
               " FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID) "
               " INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
               " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID))"
               "as temp"
               " GROUP BY VEHICLE_TYPE_NAME, VEHICLE_TYPE_ID, company_type"
               " ORDER BY company_type, VEHICLE_TYPE_ID;")
        mycursor.execute(sql1)

        print("\nVehicle Usage report format 1 \n")


        companyT_temp = ""

        for x in mycursor:
            total_distance = x[0]
            vehicle_type_name = x[2]
            company_type = x[3]

            if companyT_temp == company_type:
                print("<{0}> \nTotal Distance: {1}"
                      .format(vehicle_type_name, total_distance))
            else:
                print("{0} \n{1} \n{2} \n<{3}> \nTotal Distance: {4}"
                      .format(star, company_type, star, vehicle_type_name, total_distance))
            companyT_temp = company_type

    else:
        # Format 2
        sql2 = ("SELECT SUM(Distance) As Total_Distance, COMPANY_NAME, COMPANY_ID VEHICLE_TYPE_ID, VEHICLE_TYPE_NAME,company_type "
               " FROM ( SELECT V.VEHICLE_ID, VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, VU.DISTANCE,"
               "C.COMPANY_NAME, C.COMPANY_ID, C.COMPANY_TYPE"
               " FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID) "
               " INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
               " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID))"
               "as temp"
               " GROUP BY VEHICLE_TYPE_NAME, COMPANY_ID, VEHICLE_TYPE_ID, company_type"
               " ORDER BY COMPANY_ID, VEHICLE_TYPE_ID;")
        mycursor.execute(sql2)

        companyN_temp = ""
        companyT_temp = ""
        print("\nVehicle Usage report format 2 ")
        for x in mycursor:
            total_distance = x[0]
            company_name = x[1]
            vehicle_type_name = x[3]
            company_type = x[4]

            if companyT_temp == company_type:
                if companyN_temp == company_name:
                    print("{0} Total Distance: {1}".format(vehicle_type_name, total_distance))
                else:
                    print("\n<{0}> \n{1} Total Distance: {2}".format(company_name, vehicle_type_name, total_distance))
                companyN_temp = company_name

            else:
                print("\n{0} \n{1} \n{2}".format(star,company_type,star))
                if companyN_temp == company_name:
                    print("{0} Total Distance: {1}".format( vehicle_type_name, total_distance ))
                else:
                    print("\n<{0}> \n{1} Total Distance: {2}".format(company_name, vehicle_type_name, total_distance ))
                companyN_temp = company_name
            companyT_temp = company_type

    print("\n~~~~ MENU ~~~~")
    print("\n1. Show data(format 1) \n2. Show data(format 2) \n3. Exit")
    option = int(input("Enter your option ==> "))

else:
    print("\nExit. \nThank you!")


