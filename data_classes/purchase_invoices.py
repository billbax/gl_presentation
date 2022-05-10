import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from excel_writer.excel_writer_class import ExcelWriter

CMAP_PLACEHOLDERS = ["1000 (Cmap)", "1001 (Cmap)"]


class PurchaseInvoices:
    def __init__(self, client_data, file_path):
        # Create the purchase invoices dataframe required by the import tool from the lists of default import columns
        self.purchase_inv_df = create_df.create_import_template(columns=import_columns.PURCHASE_COL)

        # Extract the purchase invoice data from the client data sheet received
        self.purchase_data_rec = create_df.read_sheet(data=client_data, sheet_name="Project Number")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.purchase_data_rec = create_df.remove_placeholders(data=self.purchase_data_rec, column_header="Project Number",
                                                               placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.purchase_inv_df = conv_funcs.remap_columns(df=self.purchase_inv_df, data=self.purchase_data_rec,
                                                        mapping_dict=remapping_dicts.PURCHASE_MAP)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.purchase_inv_df = conv_funcs.fill_columns(df=self.purchase_inv_df, fill_column_dict=fill_columns.NULL_PURCHASE_INV)

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="15. Purchase Invoices",
                    dataframe_dict={
                        "Purchase Invoices": self.purchase_inv_df,
                        }
                    )
