import mysql.connector

print("Welcome!")

print("\n~~~~ MENU ~~~~")
print("\n1. Show Vehicle Usage Data with carbon footprint (format 1) "
      "\n2. Show Vehicle Usage Data with carbon footprint (format 2) "
      "\n3. Show Vehicle info imput in Morning (5:01-11:59) "
      "\n4. Show Vehicle info imput in Afternoon (12:00-17:00) "
      "\n5. Show Vehicle info imput in Evening (17:01-20:00) "
      "\n6. Show Vehicle info imput in Night (20:01-5:00) "
      "\n7. Exit")
option = int(input("\nEnter your option ==> "))

while option >= 1 and option <= 6:

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vshare_online_additional",
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()
    star = "*****************************"

    if option == 1:
        # Format 1
        sql1 = ("SELECT SUM(Distance) As Total_Distance, VEHICLE_TYPE_ID, VEHICLE_TYPE_NAME,company_type, Estimate_carbon_amount "
               " FROM ( SELECT V.VEHICLE_ID, VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, VT.Estimate_carbon_amount, VU.DISTANCE, C.COMPANY_NAME, C.COMPANY_TYPE "
               " FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID) "
               " INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
               " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID))"
               "as temp"
               " GROUP BY VEHICLE_TYPE_NAME, VEHICLE_TYPE_ID, company_type,Estimate_carbon_amount"
               " ORDER BY company_type, VEHICLE_TYPE_ID;")
        mycursor.execute(sql1)

        print("\nVehicle Usage Data with carbon footprint (format 1)\n")


        companyT_temp = ""

        for x in mycursor:
            total_distance = x[0]
            vehicle_type_name = x[2]
            company_type = x[3]
            carbon_amt = x[4]

            if companyT_temp == company_type:
                print("<{0}> \nTotal Distance: {1} km"
                      .format(vehicle_type_name, total_distance))
                total = total_distance*carbon_amt
                print("Total Estimate Carbon Footprint: {0} g".format(total))
            else:
                print("{0} \n{1} \n{2} \n<{3}> \nTotal Distance: {4} km"
                      .format(star, company_type, star, vehicle_type_name, total_distance))
                total = total_distance * carbon_amt
                print("Total Estimate Carbon Footprint: {0} g".format(total))
            companyT_temp = company_type

    elif option == 2:
        # Format 2
        sql2 = ("SELECT SUM(Distance) As Total_Distance, COMPANY_NAME, COMPANY_ID VEHICLE_TYPE_ID, VEHICLE_TYPE_NAME,"
                "company_type, Estimate_carbon_amount "
               " FROM ( SELECT V.VEHICLE_ID, VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, VT.Estimate_carbon_amount, VU.DISTANCE,"
               "C.COMPANY_NAME, C.COMPANY_ID, C.COMPANY_TYPE"
               " FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID) "
               " INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
               " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID))"
               "as temp"
               " GROUP BY VEHICLE_TYPE_NAME, COMPANY_ID, VEHICLE_TYPE_ID, company_type, Estimate_carbon_amount"
               " ORDER BY COMPANY_ID, VEHICLE_TYPE_ID;")
        mycursor.execute(sql2)

        companyN_temp = ""
        companyT_temp = ""
        print("\nVehicle Usage Data with carbon footprint (format 2)")
        for x in mycursor:
            total_distance = x[0]
            company_name = x[1]
            vehicle_type_name = x[3]
            company_type = x[4]
            carbon_amt = x[5]

            if companyT_temp == company_type:
                if companyN_temp == company_name:
                    print("{0} Total Distance: {1} km".format(vehicle_type_name, total_distance))
                    total = total_distance * carbon_amt
                    print("Total Estimate Carbon Footprint: {0} g".format(total))

                else:
                    print("\n<{0}> \n{1} Total Distance: {2} km".format(company_name, vehicle_type_name, total_distance))
                    total = total_distance * carbon_amt
                    print("Total Estimate Carbon Footprint: {0} g".format(total))
                companyN_temp = company_name

            else:
                print("\n{0} \n{1} \n{2}".format(star,company_type,star))
                if companyN_temp == company_name:
                    print("{0} Total Distance: {1} km".format( vehicle_type_name, total_distance ))
                    total = total_distance * carbon_amt
                    print("Total Estimate Carbon Footprint: {0} g".format(total))
                else:
                    print("\n<{0}> \n{1} Total Distance: {2} km".format(company_name, vehicle_type_name, total_distance ))
                    total = total_distance * carbon_amt
                    print("Total Estimate Carbon Footprint: {0} g".format(total))
                companyN_temp = company_name
            companyT_temp = company_type

    elif option == 3:
        sql = (
            "SELECT  VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, "
            "  VU.DISTANCE, C.COMPANY_NAME, C.COMPANY_TYPE, VU.time, VU.date "
            "FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID)"
            "INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
            " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID) where time >= '5:01' and time <='11:59'"
            " GROUP BY time, VEHICLE_TYPE_NAME, VEHICLE_TYPE_ID, company_type,Estimate_carbon_amount"
            " ORDER BY time, company_type, VEHICLE_TYPE_ID;")
        mycursor.execute(sql)

        print("\nVehicle info imput in Morning (5:01-11:59)\n")

        print("%-13s %-15s %-15s %-20s %-18s" % ("TIME","DATE","COMPANY_TYPE","VEHICLE_TYPE","DISTANCE"))
        for x in mycursor:
            time = x[5]
            date = x[6]
            company_type = x[4]
            vehicle_type_name = x[0]
            distance = x[2]
            print("%-13s %-15s %-15s %-20s %-18s" % (time,date,company_type,vehicle_type_name,distance))

    elif option == 4:
        sql = (
            "SELECT  VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, "
            "  VU.DISTANCE, C.COMPANY_NAME, C.COMPANY_TYPE, VU.time, VU.date "
            "FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID)"
            "INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
            " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID) where time >= '12:00' and time <='17:00'"
            " GROUP BY time, VEHICLE_TYPE_NAME, VEHICLE_TYPE_ID, company_type,Estimate_carbon_amount"
            " ORDER BY time, company_type, VEHICLE_TYPE_ID;")
        mycursor.execute(sql)

        print("\nVehicle info imput in Afternoon (12:00-17:00) \n")


        print("%-13s %-15s %-15s %-20s %-18s" % ("TIME","DATE","COMPANY_TYPE","VEHICLE_TYPE","DISTANCE"))
        for x in mycursor:
            time = x[5]
            date = x[6]
            company_type = x[4]
            vehicle_type_name = x[0]
            distance = x[2]
            print("%-13s %-15s %-15s %-20s %-18s" % (time,date,company_type,vehicle_type_name,distance))

    elif option == 5:
        sql = (
            "SELECT  VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, "
            "  VU.DISTANCE, C.COMPANY_NAME, C.COMPANY_TYPE, VU.time, VU.date "
            "FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID)"
            "INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
            " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID) where time >= '17:01' and time <='20:00'"
            " GROUP BY time, VEHICLE_TYPE_NAME, VEHICLE_TYPE_ID, company_type,Estimate_carbon_amount"
            " ORDER BY time, company_type, VEHICLE_TYPE_ID;")
        mycursor.execute(sql)

        print("\nVehicle info imput in Evening (17:01-20:00)\n")

        print("%-13s %-15s %-15s %-20s %-18s" % ("TIME","DATE","COMPANY_TYPE","VEHICLE_TYPE","DISTANCE"))
        for x in mycursor:
            time = x[5]
            date = x[6]
            company_type = x[4]
            vehicle_type_name = x[0]
            distance = x[2]
            print("%-13s %-15s %-15s %-20s %-18s" % (time,date,company_type,vehicle_type_name,distance))

    else:
        sql = (
            "SELECT  VT.VEHICLE_TYPE_NAME, VT.VEHICLE_TYPE_ID, "
            "  VU.DISTANCE, C.COMPANY_NAME, C.COMPANY_TYPE, VU.time, VU.date "
            "FROM (((vehicle_usage VU INNER JOIN vehicle V on VU.VEHICLE_ID = V.VEHICLE_ID)"
            "INNER JOIN vehicle_type VT on VT.VEHICLE_TYPE_ID= V.VEHICLE_TYPE_ID)"
            " INNER JOIN company C on C.COMPANY_ID= VU.COMPANY_ID) where (time >= '20:01' and time <='24:00')or"
            "(time >= '00:00' and time <= '5:00')"
            " GROUP BY time, VEHICLE_TYPE_NAME, VEHICLE_TYPE_ID, company_type,Estimate_carbon_amount"
            " ORDER BY time, company_type, VEHICLE_TYPE_ID;")
        mycursor.execute(sql)

        print("\nShow Vehicle info imput in Night (20:01-5:00)\n")

        print("%-13s %-15s %-15s %-20s %-18s" % ("TIME","DATE","COMPANY_TYPE","VEHICLE_TYPE","DISTANCE"))
        for x in mycursor:
            time = x[5]
            date = x[6]
            company_type = x[4]
            vehicle_type_name = x[0]
            distance = x[2]
            print("%-13s %-15s %-15s %-20s %-18s" % (time,date,company_type,vehicle_type_name,distance))

    print("\n~~~~ MENU ~~~~")
    print("\n1. Show Vehicle Usage Data with carbon footprint (format 1) "
          "\n2. Show Vehicle Usage Data with carbon footprint (format 2) "
          "\n3. Show Vehicle info imput in Morning (5:01-11:59) "
          "\n4. Show Vehicle info imput in Afternoon (12:00-17:00) "
          "\n5. Show Vehicle info imput in Evening (17:01-20:00) "
          "\n6. Show Vehicle info imput in Night (20:01-5:00) "
          "\n7. Exit")
    option = int(input("\nEnter your option ==> "))

else:
    print("\nExit. \nThank you!")

