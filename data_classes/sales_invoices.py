import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from conversion.conversion_functions.isin_check import isin_check
from excel_writer.excel_writer_class import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks

CMAP_PLACEHOLDERS = ["1000 (Cmap)", "1001 (Cmap)", "1002 (Cmap)"]


class SalesInvoices:
    def __init__(self, client_data, project_validation, stage_validation, file_path):

        # Create the invoice dataframes required by the import tool from the list of default columns
        self.invoice_top_df = create_df.create_import_template(columns=import_columns.INVOICE_COL)
        self.invoice_breakdown_df = create_df.create_import_template(columns=import_columns.INVOICE_DET_COL)

        # Extract the invoice data
        self.invoice_data_rec = create_df.read_sheet(data=client_data, sheet_name="Invoices")

        # Remove all CMap example rows based on the (Cmap) cell identifier
        self.invoice_data_rec = create_df.remove_placeholders(data=self.invoice_data_rec, column_header="Project Number",
                                                              placeholders=CMAP_PLACEHOLDERS, )

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.invoice_breakdown_df = conv_funcs.remap_columns(df=self.invoice_breakdown_df, data=self.invoice_data_rec,
                                                             mapping_dict=remapping_dicts.INVOICE_DET_MAP)

        # Concatenate project/stage to compare against fee estimator breakdown data
        self.invoice_breakdown_df["Stage"] = self.invoice_breakdown_df[["Project", "Budget Section"]] \
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.invoice_breakdown_df = conv_funcs.fill_columns(df=self.invoice_breakdown_df, fill_column_dict=fill_columns.NULL_INV_DET)

        # Check if project exists in project data received (invoice details tab)
        self.invoice_breakdown_df = isin_check(df=self.invoice_breakdown_df, validation_df=stage_validation,
                                               check_cols=["Project"])

        # Check if stage exists in project data received
        self.invoice_breakdown_df = isin_check(df=self.invoice_breakdown_df, validation_df=stage_validation,
                                               validation_col="Stage Validation", check_cols=["Stage"])

        # Rename Stage Exists to distinguish data form when calling check_for_placeholders
        self.invoice_breakdown_df.rename({"Stage Exists": "Invoices - Stage Exists"}, axis=1, inplace=True)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.invoice_top_df = conv_funcs.remap_columns(df=self.invoice_top_df, data=self.invoice_data_rec,
                                                       mapping_dict=remapping_dicts.INVOICE_MAP)

        # Concatenate Project/Invoice Number to create a 'Combined' column to merge across datasheets
        self.invoice_breakdown_df["Combined"] = self.invoice_breakdown_df[["Project", "Date", "Invoice Number"]]\
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        self.invoice_top_df["Combined"] = self.invoice_top_df[["Project", "Date", "Invoice Number"]]\
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Drop duplicates in invoice_top_df to get sum alone
        self.invoice_top_df.drop_duplicates(subset="Combined", inplace=True)

        # Create a dataframe that contains the sum for each unique invoice
        sums_df = self.invoice_breakdown_df.groupby("Combined")["Net"].sum()
        # Merge invoice_top_df with sums_df to populate the net invoice amount with the sum
        self.invoice_top_df = self.invoice_top_df.merge(sums_df, on="Combined", how="left")

        # Populate the VAT amount column with Net * VAT rate
        self.invoice_top_df['VAT'] = self.invoice_top_df['Net'] * self.invoice_top_df['VAT Rate']
        # Replace % VAT Rates with strings that can be accepted by the import tool
        self.invoice_top_df['VAT Rate'].replace({0.2: "20%", 0: '0%'}, inplace=True)

        # Create dataframe containing company/contact/address data to merge with invoice_top_df
        address_df = project_validation.reindex(columns=["Code", "Company", "Contact", "Address"])
        # Rename Code to project to match invoice column
        address_df.rename({"Code": "Project"}, axis=1, inplace=True)
        # Merge invoice_top_df with address_df to populate client information
        self.invoice_top_df = self.invoice_top_df.merge(address_df, on="Project", how="left")

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.invoice_top_df = conv_funcs.fill_columns(df=self.invoice_top_df,
                                                      fill_column_dict=fill_columns.NULL_INV_TOP)

        # Check if project exists in project data received (invoice top level tab)
        self.invoice_top_df = isin_check(df=self.invoice_top_df, validation_df=stage_validation,
                                         check_cols=["Project"])

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="6. Sales Invoices",
                    dataframe_dict={
                        "Sales Invoices": self.invoice_top_df,
                        "Sales Invoices Detail": self.invoice_breakdown_df,
                        }
                    )

        # Run checks for placeholder values used
        check_funcs.check_for_placeholders(check_type=error_checks.inv_top_check, df=self.invoice_top_df,
                                           class_name="Invoices", file_path=file_path)

        check_funcs.check_for_placeholders(check_type=error_checks.inv_det_check, df=self.invoice_breakdown_df,
                                           file_path=file_path)
