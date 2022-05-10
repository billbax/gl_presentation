import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from conversion.conversion_functions.merge_dataframes import merge_dataframes
from conversion.conversion_functions.isin_check import isin_check
from excel_writer.excel_writer_class import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks

CMAP_PLACEHOLDERS = ["James Carr (Cmap)", "Sarah Jackson (Cmap)", "Danielle Bates (Cmap)", "Daniel May (Cmap)"]


class InternalTime:
    def __init__(self, client_data, user_validation, system_data, file_path):
        # Create the internal time dataframe required by the import tool from the lists of default columns
        self.internal_time_df = create_df.create_import_template(import_columns.TIME_COL)

        # Extract the internal time data from the client data sheet received
        self.internal_time_rec = create_df.read_sheet(data=client_data, sheet_name="Internal Time")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.internal_time_rec = create_df.remove_placeholders(data=self.internal_time_rec, column_header="Person",
                                                               placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.internal_time_df = conv_funcs.remap_columns(df=self.internal_time_df, data=self.internal_time_rec,
                                                         mapping_dict=remapping_dicts.INT_TIME_MAP)

        # Merge project_time_df with user_df to populate the role column
        self.internal_time_df = merge_dataframes(df=self.internal_time_df, merge_data=user_validation, merge_on="Person",
                                                 merge_cols=["Person", "Role"])

        # Check if person exists in user data received
        self.internal_time_df = isin_check(df=self.internal_time_df, validation_df=user_validation,
                                           validation_col="Person", check_cols=["Person"])

        # Rename Person Exists to distinguish data form when calling check_for_placeholders
        self.internal_time_df.rename({"Person Exists": "Internal - Person Exists"}, axis=1, inplace=True)

        # Check if internal code is set up in system
        self.internal_time_df = isin_check(df=self.internal_time_df, validation_df=system_data,
                                           validation_col=["Internal Code"], check_cols=["Internal Code"])

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.internal_time_df = conv_funcs.fill_columns(df=self.internal_time_df, fill_column_dict=fill_columns.NULL_INT_TIME)

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="5. Internal Time",
                    dataframe_dict={
                        "Timesheets": self.internal_time_df,
                        }
                    )

        # Run checks for placeholder values/non config internal codes used
        check_funcs.check_for_placeholders(check_type=error_checks.int_time_check, df=self.internal_time_df,
                                           class_name="Internal Time", file_path=file_path)

        check_funcs.non_config_data(df=self.internal_time_df, system_data=system_data, columns=["Internal Code"],
                                    file_path=file_path)
