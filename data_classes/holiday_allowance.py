import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from excel_writers.excel_writer import ExcelWriter

CMAP_PLACEHOLDERS = ["James Carr (Cmap)", "Sarah Jackson (Cmap)", "Danielle Bates (Cmap)", "Daniel May (Cmap)"]


class HolidayAllowance:
    def __init__(self, client_data):
        # Create the holiday allowance dataframe required by the import tool from the lists of default columns
        self.holiday_allow_df = create_df.create_import_template(import_columns.HOL_ALLOW_COL)

        # Extract the holiday allowance data from the client data sheet received
        self.holiday_data_rec = create_df.read_sheet(data=client_data, sheet_name="Users")

        # Concatenate the first/last name columns to create a full name column
        self.holiday_data_rec["Person"] = self.holiday_data_rec[["First Name", "Last Name"]]\
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.holiday_data_rec = create_df.remove_placeholders(data=self.holiday_data_rec, column_header="Last Name",
                                                              placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.holiday_allow_df = conv_funcs.remap_columns(df=self.holiday_allow_df, data=self.holiday_data_rec,
                                                         mapping_dict=remapping_dicts.HOL_ALLOWANCE_MAP)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.holiday_allow_df = conv_funcs.fill_columns(df=self.holiday_allow_df,
                                                        fill_column_dict=fill_columns.NULL_HOLIDAY_ALLOW)


        # Export dataframes to excel
        ExcelWriter(excel_file_name="16. Holiday Allowance",
                    dataframe_dict={
                        "Holiday Allowances": self.holiday_allow_df,
                        }
                    )