import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from excel_writer.excel_writer_class import ExcelWriter

CMAP_PLACEHOLDERS = ["James Carr (Cmap)", "Sarah Jackson (Cmap)", "Danielle Bates (Cmap)", "Daniel May (Cmap)"]


class Holidays:
    def __init__(self, client_data, file_path):
        # Create the holiday dataframe required by the import tool from list of default columns
        self.holiday_df = create_df.create_import_template(columns=import_columns.HOL_COL)

        # Extract the holiday data from the client data sheet received
        self.holiday_data_rec = create_df.read_sheet(data=client_data, sheet_name="Holidays - Time Off")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.holiday_data_rec = create_df.remove_placeholders(data=self.holiday_data_rec, column_header="Person",
                                                              placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.holiday_df = conv_funcs.remap_columns(df=self.holiday_df, data=self.holiday_data_rec,
                                                   mapping_dict=remapping_dicts.HOL_MAP)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.holiday_df = conv_funcs.fill_columns(df=self.holiday_df, fill_column_dict=fill_columns.NULL_HOLIDAY)

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="3. Holidays",
                    dataframe_dict={
                        "Holidays": self.holiday_df,
                        }
                    )
