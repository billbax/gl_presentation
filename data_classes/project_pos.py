import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from excel_writer.excel_writer_class import ExcelWriter
from conversion.conversion_functions.merge_dataframes import merge_dataframes

CMAP_PLACEHOLDERS = ["92384566 (Cmap)", "AD20488 (Cmap)"]


class ProjectPOs:
    def __init__(self, client_data, proj_data_rec, file_path):
        # Create the project PO dataframe required by the import tool from the lists of default columns
        self.project_pos_df = create_df.create_import_template(import_columns.PO_COL)
        self.account_po_df = create_df.create_import_template(import_columns.ACCOUNT_PO_COL)

        # Extract the PO data from the client data sheet received
        self.project_pos_rec = create_df.read_sheet(data=client_data, sheet_name="Project PO's")

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.project_pos_df = conv_funcs.remap_columns(df=self.project_pos_df, data=self.project_pos_rec,
                                                       mapping_dict=remapping_dicts.PO_MAP)

        # Merge project_pos_df with
        self.project_pos_df = merge_dataframes(df=self.project_pos_df, merge_data=proj_data_rec, merge_on="PO Number",
                                               merge_col_dict={"Project": "Project Number", "PO Number": "Purchase Order Number"},
                                               merge_cols=["Project", "PO Number"])

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="12. Project POs",
                    dataframe_dict={
                        "ProjectPOs": self.project_pos_df,
                        "AccountPOs": self.account_po_df,
                        }
                    )
