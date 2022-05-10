from datetime import datetime, timedelta

NULL_RATES = {"Live": "Y", "Order Number": "0", "Cost Rate": "0", "Default": "N"}

NULL_FE_TOP = {"Budget Type": "Budget", "AEC Detail Level": "Simple"}

NULL_FE_TAB = {"Tab Name": "Project Fees"}

NULL_FE_SECT = {"Tab Name": "Project Fees", "Probability": "100.00", "Locked": "N", "Status": "LIVE PROJECT",
                "Workstage Fee Type": "FIXED FEE"}

NULL_FE_TASK = {"Tab Name": "Project Fees", "Approved": "N", "Locked": "N", "Expense Retention": "0.00",
                "Retention": "0.00", "Percentage Complete": "0.00", "Start Date": "01 JANUARY 2022",
                "Duration": "1.00", "Probability": "100.00", "Workstage Fee Type": "FIXED FEE", "Our Fee": "0.00"}

NULL_FE_EXT = {"Tab Name": "Project Fees", "Billing Type": "BILL AS SCHEDULED"}

NULL_PROJ_DET = {"Fee Type": "AEC", "Status": "LIVE PROJECT", "Probability": "100", "Private": "N",
                 "Project Type": "Pre-CMap", "Sector": "Pre-CMap", "Lead Source": "Pre-CMap",
                 "Owner": "My First User", "Project Manager": "My First User",
                 }

NULL_INV_TOP = {"Invoice Number": "Pre-CMap", "Description": "Pre-CMap", "Date": "31/12/2021", "VAT Rate": "0%",
                "Status": "INVOICED", "Imported": "Y", }

NULL_INV_DET = {"Invoice Number": "Pre-CMap", "Budget Section": "Pre-CMap", "Date": "31/12/2021"}

NULL_COMPANY = {"Company Name": "PENDING", "Address Description": "Pending"}

NULL_CONTACTS = {"Company Name": "PENDING", "Main Contact (Y/N)": "N", "Accounts Contact (Y/N)": "N",
                 "First Name": "Pending", "Last Name": "Completion", }

NULL_PROJ_TIME = {"Overtime": "N", "Budget Tab": "Project Fees", "Person": "Pre CMap",
                  "Budget Section": "Pre-CMap", "Budget Task": "Pre-CMap", "Role": "PENDING"}

NULL_INT_TIME = {"Overtime": "N", "Role": "PENDING"}

NULL_EXPENSES = {"Claim Name": "Pre-CMap", "Status": "Paid", "Description": "Imported", "Exchange Rate": "1",
                 "Receipt": "N", "Reimburse": "N", "Imported": "Y", "Person": "My First User",
                 "Billing Type": "RETENTION", "Category": "Pre-CMap", }

NULL_PURCHASE_INV = {"Purchase Invoice Category": "Pending", "Status": "Received", "IsApproved": "Y",
                     "Approval Status": "Paid", }

NULL_USERS = {"Live User": "Y", "Start Date": "04/01/2015", "Security Group": "Academy Only", "Currency": "GBP",
              "Timesheet Week": (datetime.today() - timedelta(days=datetime.today().weekday())).strftime("%d %B %Y"),
              "Timesheet Start": "04/01/2021", "Auto Populate timesheet with time off": "N",
              "Autopopulate Timesheet": "N", "Show Overtime Panel": "N", "Nordic Overtime": "N",
              "Line Manager": "My First User", "Working Hours Per Week": "40", "Productivity Target": "0",
              "Cost Rate": "0.00", "Email": "placeholder@cmap.com", "Role": "Pending"}

NULL_HOLIDAY = {"Approved": "Y"}

NULL_HOLIDAY_ALLOW = {"Holiday Code": "Holiday", "Year": datetime.today().strftime("%Y"), }
