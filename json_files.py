import pandas as pd
from validations.web_scraper import create_driver


def open_xlsx_doc(file_name):
    """Follow file path and locate file matching the file_name passed. If no file found, print warning & return empty form
     to allow continuation of the script"""
    try:
        return pd.ExcelFile(f"{read_path}/Data Received/{file_name}")  # Todo Change to accept files rather than directory

    except FileNotFoundError:
        print(f"{file_name} not present")
        return pd.ExcelFile(f".//placeholder_files/{file_name}")


Testing = True

if Testing:
    client_name = "zz Test"
    config_data = pd.ExcelFile("Config.xlsx")
    system_df = pd.read_excel(config_data, sheet_name="Config")

else:
    client_name = input("What is the clients name? ")
    system_df = create_driver(system_id=input("What is the clients sysadmin ID? "))


read_path = f"C:/Users/Bill/Desktop/Clients/{client_name}"


# Todo Change to accept files rather than directory

event_json = {
     "client_name": client_name,
     "users_data": open_xlsx_doc("1. Users.xlsx"),
     "comp_cont_data": open_xlsx_doc("2. Companies & Contacts.xlsx"),
     "live_proj_data": open_xlsx_doc("3. Live Projects.xlsx"),
     "expenses_data": open_xlsx_doc("4. Project Expenses.xlsx"),
     "sales_inv_data": open_xlsx_doc("5. Invoices.xlsx"),
     "project_time_data": open_xlsx_doc("6. Project Time.xlsx"),
     "purchase_inv_data": open_xlsx_doc("7. Purchase Invoices.xlsx"),
     "internal_time_data": open_xlsx_doc("8. Internal Time.xlsx"),
     "system_df": system_df
    }
