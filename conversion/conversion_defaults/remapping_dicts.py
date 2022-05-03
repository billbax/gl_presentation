USERS_MAP = {"Live User": "Live User (Y/N)", "Firstname": "First Name", "Lastname": "Last Name",
             "Email": "Email", "Office": "Office", "Team": "Team", "Start Date": "Start Date",
             "Role": "Budget Role", "Line Manager": "Line Manager", "Time Off Approver": "Time Off Approver",
             "Expenses Approver": "Expense Approver", "Working Hours Per Week": "Working Hours Per Week",
             "Productivity Target": "Productivity Target", "Sales Target": "Sales Target",
             "Cost Rate": "Actual Hourly Cost Rate", "User Type": "User Type", "Mobile": "Mobile",
             "Direct Dial": "Direct Phone", "End Date": "End Date",
             "Time Off Second Approver": "Holiday Approver 2", "Time Off CC Approver": "Approver CC",
             "Exclude Public Holidays": "Exclude Public Holidays (Y/N)", "Finance System Code": "Supplier Code",
             "Job Title": "Job Title", "Person": "Person", }

HOL_MAP = {"Person": "Person", "Holiday Code": "Time Off Type", "Date": "Date", "Days": "Duration",
           "Actual Duration": "Duration", "Approved": "Status", "Notes": "Notes",
           "(TEMP) AM/PM": "AM or PM (Where half days leave occurs)",
           }

COMP_MAP = {'Company Name': "Company Name", 'Parent Company': "Parent Company", 'Telephone': "Telephone",
            'Fax': "Fax", 'Website': "Website", 'More Information': "More Information",
            'Address Description': "Address Description", 'Address line 1': "Address line 1",
            'Address line 2': "Address line 2", 'Address line 3': "Address line 3", 'Town/City': "Town/City",
            'County': "County", 'Postcode': "Postcode", 'Country': "Country",
            'Account Code': "Account Code", 'Supplier Code': "Supplier Code",
            'Payment Terms': "Payment Terms", 'Tags': "Tags",
            'Company Owner': "Company Owner", 'Twitter': "Twitter", 'LinkedIn': "LinkedIn",
            'VAT Number': "VAT Number",
            }

CONT_MAP = {'Company Name': "Company Name", 'First Name': "First Name", 'Last Name': "Last Name",
            'Job Title': "Job Title", 'Telephone': "Telephone", 'Mobile': "Mobile",
            'Email': "Email", 'Main Contact (Y/N)': "Main Contact (Y/N)",
            'Accounts Contact (Y/N)': "Accounts Contact (Y/N)", 'Company Address': "Company Address",
            'Notes': "Notes", 'Contact Owner': "Contact Owner", 'Tags': "Tags", 'Group': "Group",
            'Twitter': "Twitter", 'LinkedIn': "LinkedIn",
            }

PROJ_DET_MAP = {"Code": "Project Number", "Title": "Title", "Office": "Office", "Business Unit": "Team",
                "Company": "Company", "Contact": "Company Contact", "Project Type": "Project Type",
                "Sector": "Sector", "Lead Source": "Lead Source", "Start Date": "Start Date", "End Date": "End Date",
                "Owner": "Owner", "Project Manager": "Project Manager", "Co-Pilot": "Co-Pilot", "Date Won": "Won Date",
                "Bio": "Bio", "Private": "Private", "Won By": "Won By", "Won Value": "Fee",
                "Closed By": "Closed By", "Date Closed": "Date Closed", "PO Number": "Purchase Order Number",
                "Details": "More Information", "Placeholder Billing Companies": "Billing Companies",
                "Placeholder Default Invoice To": "Default Invoice To", "Status": "Status",
                }

PO_MAP = {"Company": "Company", "PO Number": "PO Number", "Currency": "Currency", "Amount": "Amount", }

FE_FEE_EST_MAP = {"Project": "Project Number", "Rate": "Project's Rate Card",
                  "Construction Value": "Construction Cost",
                  "Fee Percentage": "Fee Percentage", "Our Fee": "Fee",
                  }

FE_TAB_MAP = {"Project": "Project Number"}

FE_SECTION_MAP = {"Project": "Project Number", "Section Name": "Stage Name",
                  "Workstage Fee Type": "Fee Type", "Probability": "Probability", "Stage Type": "Bid Stage",
                  "Locked": "Stage Locked (Y/N)",
                  }

FE_TASKS_MAP = {"Project": "Project Number", "Section Name": "Stage Name", "Task Name": "Stage Name",
                "Start Date": "Start Date", "Duration": "Duration (in Weeks)",
                "Workstage Fee Type": "Fee Type", "Our Fee": "Fee", "Fee Percentage": "% of Fee",
                "Time Charge Cap": "Time Charge Capped Amount", "Retention": "Retention Target %",
                "Expense Retention": "Expenses Allowance %", "Percentage Complete": "Percentage Complete",
                "Locked": "Stage Locked (Y/N)", "Probability": "Probability",
                }

FE_EXT_MAP = {"Project": "Project Number", "Section Name": "Stage Name", "External Name": "Additional Name",
              "Cost Price": "Cost Price", "Sale Price": "Sale Price", "Actual Price": "Sale Price",
              "Calculation Type": "Calculation Type", "Billing Type": "Billing Type",
              }

INVOICE_MAP = {'Project': "Project Number", 'Invoice Number': "Invoice Number",
               'Date': "Invoice Date", 'VAT Rate': "VAT Rate", 'Description': "Invoice Number",
               'Currency': "Currency", 'Status': "Invoice Status", 'Exchange Rate': "Exchange Rate",
               }

INVOICE_DET_MAP = {'Project': "Project Number", 'Date': "Invoice Date", 'Invoice Number': "Invoice Number",
                   'Net': "Net Amount", 'Budget Section': "Stage Name", 'Budget External': "Additional Name",
                   "More Information": "Description"
                   }

TIME_MAP = {'Date': "Date", 'Project': "Project Number", 'Person': "Person",
            'Budget Section': "Stage Name", 'Budget Task': "Stage Name", 'Hours': "Hours",
            'Notes': "Notes", 'Invoice': "Invoice Number (if Time Charge and Billed)",
            'Overtime': "Additional Time (Y/N)",
            }

INT_TIME_MAP = {'Date': "Date", 'Internal Code': "Internal Code", 'Person': "Person",
                'Hours': "Hours", 'Notes': "Notes", 'Overtime': "Additional Time (Y/N)",
                }

EXPENSE_MAP = {'Person': "Person", 'Submission Date': "Date", 'Category': "Category",
               'Description': "Notes", 'Project': "Project Number",
               'Budget External': "Additional Name \n(Only if Part of an Allowance)",
               'Billing Type': "Handled Type", 'Invoice': "Invoice Number Included On \n(If Chargeable)",
               'Claim Date': "Date", 'Currency': "Currency", "User Currency": "Currency",
               'Net': "Net Amount", 'VAT Rate': "VAT Rate", 'Miles': "Miles", 'Mileage Rate': "Mileage Rate",
               }

PURCHASE_MAP = {'Project': "Project Number", 'Budget Section': "Stage Name",
                'Budget External': "Additional Name", 'Supplier': "Supplier",
                'Date': "Date",
                'Invoice Number': "Invoice Number", 'Internal Reference': "Internal Reference",
                'Description': "Description",
                'Currency': "Currency", 'Net': "Net Amount",
                'VAT Rate': "VAT Rate",
                }

HOL_ALLOWANCE_MAP = {"Person": "Person", "Days": "Holiday Allowance", }
