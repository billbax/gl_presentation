import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from data_classes.custom_fields import CustomFields
from conversion.conversion_defaults.standard_cols import STANDARD_PROJ_COLS
from conversion.conversion_functions.merge_dataframes import merge_dataframes
from conversion.conversion_functions.isin_check import isin_check
from excel_writer.excel_writer_class import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks

CMAP_PLACEHOLDERS = ["1000 (Cmap)", "1001 (Cmap)", "1002 (Cmap)"]


class ProjectDetails:
    def __init__(self, client_data, user_validation, comp_validation, cont_validation, system_data, file_path):
        # Create the fee estimator dataframes required by the import tool from the lists of default columns
        self.proj_det_df = create_df.create_import_template(import_columns.PROJ_DET_COL)

        # Extract the project details data from the client data sheet received
        self.proj_det_rec = create_df.read_sheet(data=client_data, sheet_name="Projects")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.proj_det_rec = create_df.remove_placeholders(data=self.proj_det_rec, column_header="Project Number",
                                                          placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.proj_det_df = conv_funcs.remap_columns(df=self.proj_det_df, data=self.proj_det_rec,
                                                    mapping_dict=remapping_dicts.PROJ_DET_MAP)

        # Merge proj_det_df with comp_df to populate the 'Address' column
        self.proj_det_df = merge_dataframes(df=self.proj_det_df, merge_data=comp_validation, merge_on="Company",
                                            merge_col_dict={"Company": "Company Name", "Address": "Address Description"},
                                            merge_cols=["Company", "Address"])

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.proj_det_df = conv_funcs.fill_columns(df=self.proj_det_df, fill_column_dict=fill_columns.NULL_PROJ_DET)

        # If project 'Status' == 'Live Project', populate 'Won By' & 'Date Won' columns

        # If project 'Status' == 'Closed Project', populate 'Closed By' & 'Date Closed' columns
        self.proj_det_df["Closed By"].where(self.proj_det_df["Status"] != "Closed Project",
                                            self.proj_det_df["Project Manager"], inplace=True)

        self.proj_det_df["Date Closed"].where(self.proj_det_df["Status"] != "Closed Project",
                                              self.proj_det_df["End Date"], inplace=True)

        # Check if any custom fields are present and create a dataframe if True
        self.project_custom_fields = CustomFields(client_data=self.proj_det_rec, len_check=1,
                                                  standard_cols=STANDARD_PROJ_COLS)

        # Check if the pm/co-pilot/owner exist in users data received
        self.proj_det_df = isin_check(df=self.proj_det_df, validation_df=user_validation, validation_col="Person",
                                      check_cols=["Project Manager", "Co-Pilot", "Owner"])

        # Check if the project's company exist in c&c data received
        self.proj_det_df = isin_check(df=self.proj_det_df, validation_df=comp_validation, validation_col="Company Name",
                                      check_cols=["Company"])

        # Check if the project's contact exist in c&c data received
        self.proj_det_df = isin_check(df=self.proj_det_df, validation_df=cont_validation, validation_col="Contact",
                                      check_cols=["Contact"])

        # Check if project type/sector exist within the system
        self.proj_det_df = isin_check(df=self.proj_det_df, validation_df=system_data,
                                      check_cols=["Project Type", "Sector"])

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="13. Projects",
                    dataframe_dict={
                        "Projects": self.proj_det_df,
                        }
                    )

        ExcelWriter(file_path=file_path,
                    excel_file_name="8. Custom Fields",
                    dataframe_dict={
                        "Project - Custom Fields": self.project_custom_fields.cf_df,
                        }
                    )

        # Run checks for placeholder values/non config project types/sector used
        check_funcs.check_for_placeholders(check_type=error_checks.proj_det_check, df=self.proj_det_df,
                                           class_name="Project Details", file_path=file_path)

        check_funcs.non_config_data(df=self.proj_det_df, system_data=system_data, columns=["Project Type", "Sector"],
                                    file_path=file_path)
