import pandas as pd
from data_classes.users import Users
from data_classes.holidays import Holidays
from data_classes.holiday_allowance import HolidayAllowance
from data_classes.comp_contacts import CompAndContacts
from data_classes.internal_time import InternalTime
from data_classes.project_time import ProjectTime

from data_classes.expenses import Expenses
from data_classes.purchase_invoices import PurchaseInvoices
from data_classes.project_details import ProjectDetails
from data_classes.project_fees import ProjectFees
from data_classes.project_pos import ProjectPOs
from data_classes.rate_cards import RateCards
from data_classes.sales_invoices import SalesInvoices
from validations.web_scraper import create_driver


def open_xlsx_doc(file_name):
    """Follow file path and locate file matching the file_name passed. If no file found, print warning & return empty form
     to allow continuation of the script"""
    try:
        return pd.ExcelFile(f"{file_path}/Data Received/{file_name}")

    except FileNotFoundError:
        print(f"{file_name} not present")
        return pd.ExcelFile(f".//placeholder_files/{file_name}")


# client_name = input("What is the clients name? ")

Testing = False

if Testing:
    client_name = "zz Test"
    file_path = f"C:/Users/Bill/Desktop/Clients/{client_name}"
    config_data = pd.ExcelFile("Config.xlsx")
    system_df = pd.read_excel(config_data, sheet_name="Config")
else:
    client_name = input("What is the clients name? ")
    file_path = f"C:/Users/Bill/Desktop/Clients/{client_name}"
    system_df = create_driver(system_id=input("What is the clients sysadmin ID? "))

# Open all client files to create a pandas instance that can be passed to the data_classes for conversion.
# If file not found returns an empty form with matching column names to allow script to continue.
users_data = open_xlsx_doc("1. Users.xlsx")
comp_cont_data = open_xlsx_doc("2. Companies & Contacts.xlsx")
live_proj_data = open_xlsx_doc("3. Live Projects.xlsx")
expenses_data = open_xlsx_doc("4. Project Expenses.xlsx")
sales_inv_data = open_xlsx_doc("5. Invoices.xlsx")
project_time_data = open_xlsx_doc("6. Project Time.xlsx")
purchase_inv_data = open_xlsx_doc("7. Purchase Invoices.xlsx")
internal_time_data = open_xlsx_doc("8. Internal Time.xlsx")


users = Users(client_data=users_data, system_data=system_df, file_path=file_path)

holidays = Holidays(client_data=users_data, file_path=file_path)

holiday_allowances = HolidayAllowance(client_data=users_data, file_path=file_path)

comp_contacts = CompAndContacts(client_data=comp_cont_data, file_path=file_path)

proj_details = ProjectDetails(client_data=live_proj_data, user_validation=users.users_df, system_data=system_df,
                              comp_validation=comp_contacts.company_df, cont_validation=comp_contacts.contact_df,
                              file_path=file_path)

project_fees = ProjectFees(client_data=live_proj_data, project_validation=proj_details, file_path=file_path)

rate_cards = RateCards(client_data=live_proj_data, file_path=file_path)

project_pos = ProjectPOs(client_data=live_proj_data, file_path=file_path)

project_time = ProjectTime(client_data=project_time_data, user_validation=users.users_df,
                           stage_validation=project_fees.fe_section_df, file_path=file_path)

internal_time = InternalTime(client_data=internal_time_data, user_validation=users.users_df, system_data=system_df,
                             file_path=file_path)

sales_invoices = SalesInvoices(client_data=sales_inv_data, project_validation=proj_details.proj_det_df,
                               stage_validation=project_fees.fe_section_df, file_path=file_path)

purchase_invoices = PurchaseInvoices(client_data=purchase_inv_data, file_path=file_path)

expenses = Expenses(client_data=expenses_data, system_data=system_df, file_path=file_path)
