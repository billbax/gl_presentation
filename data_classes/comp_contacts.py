import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from data_classes.custom_fields import CustomFields
from conversion.conversion_defaults.standard_cols import STANDARD_COMP_COLS, STANDARD_CONT_COLS
from excel_writer.excel_writer_class import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks

CMAP_PLACEHOLDERS = ["CMAP Software (Cmap)", "XYZ Ltd (Cmap)", "ABC Plc (Cmap)"]


class CompAndContacts:
    def __init__(self, client_data, file_path):
        # Create the company/contact dataframes required by the import tool from the lists of default import columns
        self.company_df = create_df.create_import_template(columns=import_columns.COMP_COL)
        self.contact_df = create_df.create_import_template(columns=import_columns.CONT_COL)

        # Extract the company/contact data received from the client data sheet received
        self.comp_data_rec = create_df.read_sheet(data=client_data, sheet_name="Company")
        self.cont_data_rec = create_df.read_sheet(data=client_data, sheet_name="Contacts")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.comp_data_rec = create_df.remove_placeholders(self.comp_data_rec, column_header="Company Name",
                                                           placeholders=CMAP_PLACEHOLDERS)
        self.cont_data_rec = create_df.remove_placeholders(self.cont_data_rec, column_header="Company Name",
                                                           placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.company_df = conv_funcs.remap_columns(df=self.company_df, data=self.comp_data_rec,
                                                   mapping_dict=remapping_dicts.COMP_MAP)
        self.contact_df = conv_funcs.remap_columns(df=self.contact_df, data=self.cont_data_rec,
                                                   mapping_dict=remapping_dicts.CONT_MAP)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.company_df = conv_funcs.fill_columns(df=self.company_df, fill_column_dict=fill_columns.NULL_COMPANY)
        self.contact_df = conv_funcs.fill_columns(df=self.contact_df, fill_column_dict=fill_columns.NULL_CONTACTS)

        # Concatenate contacts first/last name to create a 'Contact' column to allow validation in other classes
        self.contact_df["Contact"] = self.contact_df[["First Name", "Last Name"]]\
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Check if any custom fields are present and create a dataframe if True
        self.company_custom_fields = CustomFields(client_data=self.comp_data_rec, len_check=1,
                                                  standard_cols=STANDARD_COMP_COLS)

        self.contact_custom_fields = CustomFields(client_data=self.cont_data_rec, len_check=2,
                                                  standard_cols=STANDARD_CONT_COLS)

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="2. Companies & Contacts",
                    dataframe_dict={
                        "Company": self.company_df,
                        "Contact": self.contact_df,
                        }
                    )

        ExcelWriter(file_path=file_path,
                    excel_file_name="8. Custom Fields",
                    dataframe_dict={
                        "Account - Custom Fields": self.company_custom_fields.cf_df,
                        "Contact - Custom Fields": self.contact_custom_fields.cf_df,
                        }
                    )

        # Run checks for placeholder values used
        check_funcs.check_for_placeholders(check_type=error_checks.comp_check, df=self.company_df,
                                           class_name="Companies & Contacts", file_path=file_path)

        check_funcs.check_for_placeholders(check_type=error_checks.cont_check, df=self.contact_df, file_path=file_path)
