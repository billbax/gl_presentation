import tempfile
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
from send_email.send_email import send_email
from json_files import event_json


file_temp_direct = tempfile.TemporaryDirectory()
file_temp_dir_name = file_temp_direct.name
file_path = file_temp_dir_name


users = Users(client_data=event_json["users_data"], system_data=event_json["system_df"], file_path=file_path)

holidays = Holidays(client_data=event_json["users_data"], file_path=file_path)

holiday_allowances = HolidayAllowance(client_data=event_json["users_data"], file_path=file_path)

comp_contacts = CompAndContacts(client_data=event_json["comp_cont_data"], file_path=file_path)

proj_details = ProjectDetails(client_data=event_json["live_proj_data"], user_validation=users.users_df, system_data=event_json["system_df"],
                              comp_validation=comp_contacts.company_df, cont_validation=comp_contacts.contact_df,
                              file_path=file_path)

project_fees = ProjectFees(client_data=event_json["live_proj_data"], project_validation=proj_details, file_path=file_path)

rate_cards = RateCards(client_data=event_json["live_proj_data"], file_path=file_path)

project_pos = ProjectPOs(client_data=event_json["live_proj_data"], proj_data_rec=proj_details.proj_det_rec, file_path=file_path)

project_time = ProjectTime(client_data=event_json["project_time_data"], user_validation=users.users_df,
                           stage_validation=project_fees.fe_section_df, file_path=file_path, system_data=event_json["system_df"])

internal_time = InternalTime(client_data=event_json["internal_time_data"], user_validation=users.users_df,
                             system_data=event_json["system_df"], file_path=file_path)

sales_invoices = SalesInvoices(client_data=event_json["sales_inv_data"], project_validation=proj_details.proj_det_df,
                               stage_validation=project_fees.fe_section_df, file_path=file_path)

purchase_invoices = PurchaseInvoices(client_data=event_json["purchase_inv_data"], project_validation=project_fees.fe_top_lvl_df,
                                     file_path=file_path)

expenses = Expenses(client_data=event_json["expenses_data"], system_data=event_json["system_df"],
                    project_validation=project_fees.fe_top_lvl_df, file_path=file_path)

send_email(temporary_directory=file_temp_dir_name, to_addr="usert6310@gmail.com", client=event_json["client_name"])
