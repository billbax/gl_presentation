import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from conversion.conversion_defaults.standard_cols import STANDARD_USER_COLS
from data_classes.custom_fields import CustomFields
from conversion.conversion_functions.isin_check import isin_check
from excel_writers.excel_writer import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks

CMAP_PLACEHOLDERS = ["James Carr (Cmap)", "Sarah Jackson (Cmap)", "Danielle Bates (Cmap)", "Daniel May (Cmap)"]


class Users:
    def __init__(self, client_data, system_data):
        # Create the user dataframe required by the import tool from the lists of default columns
        self.users_df = create_df.create_import_template(import_columns.USERS_COL)

        # Extract the user data from the client data sheet received
        self.user_data_rec = create_df.read_sheet(data=client_data, sheet_name="Users")

        # Concatenate first/last name to create a 'Person' to allow validation/merges in other classes
        self.user_data_rec["Person"] = self.user_data_rec[["First Name", "Last Name"]]\
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.user_data_rec = create_df.remove_placeholders(data=self.user_data_rec, column_header="Person",
                                                           placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.users_df = conv_funcs.remap_columns(df=self.users_df, data=self.user_data_rec,
                                                 mapping_dict=remapping_dicts.USERS_MAP)

        # Check if user set up as admin in Cmap if True set security group to full access
        self.users_df["Security Group"].where(~self.users_df["Person"].isin(system_data["Person"]),
                                              "1. Full Access", inplace=True)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.users_df = conv_funcs.fill_columns(df=self.users_df, fill_column_dict=fill_columns.NULL_USERS)

        # Fill holiday/expense approver with line manager if null
        self.users_df["Time Off Approver"].fillna(self.users_df["Line Manager"], inplace=True)
        self.users_df["Expenses Approver"].fillna(self.users_df["Line Manager"], inplace=True)

        # Check if users role exists within the system
        self.users_df = isin_check(df=self.users_df, validation_df=system_data, validation_col="Role",
                                   check_cols=["Role"])

        # Check if any custom fields are present and create a dataframe if True
        self.user_custom_fields = CustomFields(client_data=self.user_data_rec, len_check=1,
                                               standard_cols=STANDARD_USER_COLS)

        # Convert columns to datetime
        self.users_df[['End Date', "Start Date", "Timesheet Start", "Timesheet Week"]] = \
            self.users_df[['End Date', "Start Date", "Timesheet Start", "Timesheet Week"]].astype('datetime64[ns]')

        # Export dataframes to excel
        ExcelWriter(excel_file_name="1. Users",
                    dataframe_dict={
                        "Users": self.users_df,
                        }
                    )

        ExcelWriter(excel_file_name="8. Custom Fields",
                    dataframe_dict={
                        "User - Custom Fields": self.user_custom_fields.cf_df,
                        }
                    )

        # Run checks for placeholder values used/data not matching config data
        check_funcs.check_for_placeholders(check_type=error_checks.user_checks, df=self.users_df,
                                           class_name="Users")

        check_funcs.non_config_data(df=self.users_df, system_data=system_data, columns=["Role"])
