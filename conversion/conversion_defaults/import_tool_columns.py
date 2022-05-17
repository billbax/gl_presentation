USERS_COL = ["Live User", "Firstname", "Lastname", "Person", "Email", "Office", "Team",
             "Role", "Role Exists", "Job Title", "Line Manager", "Time Off Approver", "Expenses Approver",
             "Working Hours Per Week", "Productivity Target", "Sales Target", "Cost Rate",
             "Currency", "User Type",  "Mobile", "Auto Populate timesheet with time off",
             "Direct Dial", "Security Group", "Start Date", "End Date", "Timesheet Start", "Timesheet Week",
             "Time Off Second Approver", "Time Off CC Approver", "Exclude Public Holidays",
             "Holiday Start Date", "Timesheet Approver",  "Timesheet Second Approver",
             "Autopopulate Timesheet", "Budget Approval Min", "Budget Approval Max",
             "Finance System Code", "External Reference", "Nordic Overtime",
             "Show Overtime Panel", "Locale", "TimeZone"
             ]

USER_FIG_COL = ["Person", "Role", "Role Exists", "Start Date", "End Date", "Working Hours", "Productivity Target", "Cost Rate"]

CLASH_COL = ["Person", "Clashes With"]

USER_DELEGATES_COL = ["Person", "Delegate"]


HOL_COL = ["Person", "Holiday Code", "Date", "Days", "Actual Duration", "Approved", "Notes",
           "(TEMP) AM/PM"]

HOL_ALLOW_COL = ["Person", "Holiday Code", "Year", "Days", "Notes", "Is Accrual", "Days Accrued"]

COMP_COL = ['Company Name', 'Parent Company', 'Telephone', 'Fax', 'Website', 'More Information',
            'Address Description', 'Address line 1', 'Address line 2', 'Address line 3', 'Town/City',
            'County', 'Postcode', 'Country', 'Account Code', 'Supplier Code', 'Payment Terms', 'Tags',
            'Company Owner', 'Twitter', 'LinkedIn', 'VAT Number']

CONT_COL = ['Company Name', 'First Name', 'Last Name', 'Job Title', 'Telephone', 'Fax', 'Mobile', 'Email',
            'Main Contact (Y/N)', 'Accounts Contact (Y/N)', 'Company Address', 'Notes', 'Contact Owner',
            'Tags', 'Group', 'Twitter', 'LinkedIn']

PROJ_DET_COL = ["Fee Type", "Code", "Title", "Office", "Business Unit", "Currency",
                "Company", "Company Exists", "Contact", "Contact Exists",
                "Status", "Probability", "Project Type", "Project Type Exists", "Sector", "Sector Exists",
                "Lead Source", "Start Date", "End Date",
                "Owner", "Owner Exists", "Project Manager", "Project Manager Exists", "Co-Pilot", "Co-Pilot Exists",
                "Date Won", "Stage", "Bio", "Private", "Won By",
                "Won Value", "Closed By", "Date Closed", "Reason For Loss", "Date Lost", "Reason For Loss Notes",
                "Expense Item Multiplier", "Mileage Multiplier", "PO Number", "Budget Fee Type", "Fee Forecast Type",
                "Additional Forecast Type", "Fee Revenue History Type", "Additional Revenue History Type", "RAG",
                "Direct Cost Percentage", "Project Account", "Campaign", "Phasing By Type", "Invoicing Type", "Details",
                "Placeholder Billing Companies", "Placeholder Default Invoice To"]

PO_COL = ["PO Number", "Company", "Currency", "Amount"]

ACCOUNT_PO_COL = ["PO Number", "Company", "Currency", "Amount", "Start Date", "End Date"]

FE_COL = ["Project", "Budget Type", "AEC Detail Level", "Rate",
          "Construction Value", "Fee Percentage", "Our Fee", "Gross Fee",
          "Our Fee Type Calculation", "Square Feet", "Price Per Square Foot",
          "Approved", "Approved By", "Date Approved"]

FE_TAB_COL = ["Project", "Tab Name"]

FE_SECT_COL = ["Project", "Tab Name", "Section Name", "Workstage Fee Type",
               "Probability", "Target Profit Margin", "Stage Type", "Locked", "Closed", "Closed By",
               "Closed Date", "Fee Forecast Type", "Fee Revenue History Type",
               "Additional Revenue History Type", "Tags"]

FE_TASK_COL = ["Project", "Tab Name", "Section Name", "Task Name", "Start Date", "Duration",
               "Workstage Fee Type", "Probability", "Our Fee", "Fee Percentage", "Time Charge Cap",
               "Retention", "Expense Retention", "Percentage Complete", "Locked", "Outside Fee",
               "Notes", "Date Won", "Won By", "Cost Plus", "Approved"]

FE_EXT_COL = ["Project", "Tab Name", "Section Name", "External Name", "Cost Price", "Sale Price",
              "Actual Price", "Calculation Type", "Billing Type", "Purchase Order", "External Type"]

FE_UNITS_COL = ["Project", "Tab Name", "Section Name", "Task Name", "Role", "Hours"]

FE_ADJUST_COL = ["Project", "Tab Name", "Adjustment Name", "Value"]

INVOICE_COL = ['Project', 'Invoice Template', 'Invoice Number',
               'Description', 'Date', 'VAT', 'VAT Rate', 'Currency', 'PO Number', 'Status',
               'Notes', 'Imported', 'Percentage', 'Already Invoiced', 'Date Paid', 'Alternate Currency',
               'Exchange Rate', 'Amount Paid']

INVOICE_DET_COL = ['Project', 'Date', 'Invoice Number', 'Information', 'Net', 'Entity Type',
                   'Budget Section',  'Combined', 'Budget External', 'Notes', 'More Information']

TIME_COL = ['Date', 'Project', 'Internal Code', 'Internal Code Exists', 'Person', 'Person Exists', 'Budget Tab', 'Budget Section',
            'Budget Task', 'Hours', 'Notes', 'Billable', 'Billable Hours', 'Invoice', 'Overtime',
            'Paid Overtime', 'Paid Overtime Approved By', 'Approved', 'Approved By', 'Date Approved',
            'Recognised', 'Recognised Submitted Date', 'Recognised Hours', 'Recognised Submitted By',
            'Recognised Notes', 'Hours Recognised', 'Date Recognised', 'Work Activity']

EXPENSE_COL = ['Claim Name', 'Person', 'User Currency', 'Status', 'Submission Date', 'Category', 'Category Exists',
               'Description', 'Project', 'Budget Tab', 'Budget Section', 'Budget External',
               'Billing Type', 'Invoice', 'Internal Code', 'Claim Date', 'Currency',
               'Exchange Rate', 'Net', 'VAT Rate', 'Miles', 'Mileage Rate', 'Receipt',
               'Reimburse', 'Imported']

PURCHASE_COL = ['Project', 'Budget Tab', 'Budget Section', 'Budget External', 'Supplier', 'Date',
                'Invoice Number', 'Internal Reference', 'Description', 'Currency', 'Net',
                'VAT Rate', 'VAT', 'Purchase Invoice Category', 'Purchase Order', 'Status',
                'IsApproved', 'Approval Status', 'Invoice Amount Currency', 'Invoice Amount Net',
                'Invoice Amount VAT Rate', 'Invoice Amount VAT', 'Nominal Code', 'Posted Date',
                'Purchase Invoice Batch', 'Approved By', 'Date Approved', 'Imported', 'Imported By',
                'Date Imported', 'Rejected By', 'Date Rejected', 'Rejected Reason', 'Last Exported By',
                'Last Exported Date']

PURCHASE_CAT_COL = ['Name', 'Order No']

PURCHASE_BATCH_COL = ['Name', 'Office', 'Submitted']
