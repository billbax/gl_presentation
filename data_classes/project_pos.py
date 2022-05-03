import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from excel_writers.excel_writer import ExcelWriter

CMAP_PLACEHOLDERS = ["92384566 (Cmap)", "AD20488 (Cmap)"]


class ProjectPOs:
    def __init__(self, client_data):
        # Create the project PO dataframe required by the import tool from the lists of default columns
        self.project_pos_df = create_df.create_import_template(import_columns.PO_COL)

        # Extract the PO data from the client data sheet received
        self.project_pos_rec = create_df.read_sheet(data=client_data, sheet_name="Project PO's")

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.project_pos_df = conv_funcs.remap_columns(df=self.project_pos_df, data=self.project_pos_rec,
                                                       mapping_dict=remapping_dicts.PO_MAP)


        # Export dataframes to excel
        ExcelWriter(excel_file_name="12. Project POs",
                    dataframe_dict={
                        "Project POs": self.project_pos_df,
                        }
                    )
