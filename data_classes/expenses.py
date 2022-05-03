import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from conversion.conversion_functions.isin_check import isin_check
from excel_writers.excel_writer import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks


CMAP_PLACEHOLDERS = ["1000 (Cmap)", "1001 (Cmap)"]


class Expenses:
    def __init__(self, client_data, system_data):
        # Create the expenses dataframe required by the import tool from the lists of default import columns
        self.expenses_df = create_df.create_import_template(columns=import_columns.EXPENSE_COL)

        # Extract the expenses data received from the client data sheet. If sheet not found return empty dataframe
        self.expenses_data_rec = create_df.read_sheet(data=client_data, sheet_name="Project Expenses")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.expenses_data_rec = create_df.remove_placeholders(data=self.expenses_data_rec, column_header="Project Number",
                                                               placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.expenses_df = conv_funcs.remap_columns(df=self.expenses_df, data=self.expenses_data_rec,
                                                    mapping_dict=remapping_dicts.EXPENSE_MAP)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.expenses_df = conv_funcs.fill_columns(df=self.expenses_df, fill_column_dict=fill_columns.NULL_EXPENSES)

        # Check if expense category is set up within the system
        self.expenses_df = isin_check(df=self.expenses_df, validation_df=system_data,
                                      check_cols=["Category"])

        # Export dataframes to excel
        ExcelWriter(excel_file_name="10. Expenses",
                    dataframe_dict={
                        "Expenses": self.expenses_df,
                        }
                    )

        # Run checks for placeholder values/non config internal codes used
        check_funcs.check_for_placeholders(check_type=error_checks.expenses_check, df=self.expenses_df,
                                           class_name="Expenses")

        check_funcs.non_config_data(df=self.expenses_df, system_data=system_data, columns=["Category"])
