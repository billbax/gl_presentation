import tkinter.filedialog as fd
import os
import pandas as pd
from tkinter import *
from tkinter import ttk
from main import main_loop
from validations.web_scraper import create_driver

# Empty tuple to be populated with user selected files later
selected_files = ()
# Define if the function is being run as a test. If True use 'Testing System Data.xlsx' instead of creating selenium driver
Testing = False


def open_xlsx_doc(file_name, path):
    """Follow file path and locate file matching the 'file_name' variable passed. If no file found, print warning & return empty form
     to allow continuation of the script"""
    try:
        return pd.ExcelFile(f"{path}/{file_name}")

    except FileNotFoundError:
        print(f"{file_name} not present")
        return pd.ExcelFile(f".//placeholder_files/{file_name}")


def choose_files():
    """Open a pop up window to select the files that should be passed to the script"""
    global selected_files
    selected_files = fd.askopenfilenames(parent=root, title='Choose a file')

    #  TODO create a zip file and upload to aws s3 service
    # zip_obj = ZipFile("Files.zip", "w")
    # for file in selected_files:
    #     zip_obj.write(filename=file, arcname=os.path.basename(file))


def create_pop_up():
    # Pop up for confirmation that script is running
    top = Toplevel(root)
    top.geometry("350x90")
    top.title("Script Executed")
    Label(top, text="Process Completed, Please Check Your Email.", font="Calibri 12").place(x=20, y=25)


def submit_button():
    # Get the path for the files selected to be used by the open_xlsx_doc function
    try:
        directory_route = os.path.dirname(selected_files[0])
        client_name = client_name_entry.get()
        sysadmin_id = sysadmin_id_entry.get()

        # If 'Testing' variable is True use 'Testing System Data.xlsx' as placeholder system data
        if Testing:
            config_data = pd.ExcelFile("Testing System Data.xlsx")
            system_df = pd.read_excel(config_data, sheet_name="Config")

        # Else init selenium driver to scrape all data
        else:
            system_df = create_driver(system_id=sysadmin_id)

        event_json = {
            "client_name": client_name,
            "users_data": open_xlsx_doc("1. Users.xlsx", path=directory_route),
            "comp_cont_data": open_xlsx_doc("2. Companies & Contacts.xlsx", path=directory_route),
            "live_proj_data": open_xlsx_doc("3. Projects.xlsx", path=directory_route),
            "expenses_data": open_xlsx_doc("4. Project Expenses.xlsx", path=directory_route),
            "sales_inv_data": open_xlsx_doc("5. Invoices.xlsx", path=directory_route),
            "project_time_data": open_xlsx_doc("6. Project Time.xlsx", path=directory_route),
            "purchase_inv_data": open_xlsx_doc("7. Purchase Invoices.xlsx", path=directory_route),
            "internal_time_data": open_xlsx_doc("8. Internal Time.xlsx", path=directory_route),
            "system_df": system_df
        }
        main_loop(event_json)
        create_pop_up()

    except IndexError:
        print("Missing required variable")


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Client Name").grid(column=0, row=0)
client_name_entry = ttk.Entry(frm)
client_name_entry.grid(column=1, row=0)

ttk.Label(frm, text="Sysadmin ID").grid(column=0, row=1)
sysadmin_id_entry = ttk.Entry(frm)
sysadmin_id_entry.grid(column=1, row=1)

ttk.Label(frm, text="Pick Your Files").grid(column=0, row=2)
ttk.Button(frm, text="Select Files", command=choose_files).grid(column=1, row=2)
ttk.Button(frm, text="Execute", command=submit_button).grid(column=0, row=3)
root.mainloop()
