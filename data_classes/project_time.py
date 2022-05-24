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


class ProjectTime:
    def __init__(self, client_data, user_validation, stage_validation, file_path, system_data):
        # Create the project time dataframe required by the import tool from the lists of default columns
        self.project_time_df = create_df.create_import_template(import_columns.TIME_COL)

        # Extract the project time & user figures data from the client data sheet received
        self.project_time_rec = create_df.read_sheet(data=client_data, sheet_name="Project Time")
        self.time_user_figs_rec = create_df.read_sheet(data=client_data, sheet_name="User Figures")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.project_time_rec = create_df.remove_placeholders(data=self.project_time_rec, column_header="Person",
                                                              placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dicts
        self.project_time_df = conv_funcs.remap_columns(df=self.project_time_df, data=self.project_time_rec,
                                                        mapping_dict=remapping_dicts.TIME_MAP)

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.project_time_df = conv_funcs.fill_columns(df=self.project_time_df, fill_column_dict=fill_columns.NULL_PROJ_TIME)

        # Concatenate project/stage to compare against fee estimator breakdown data
        self.project_time_df["Time - Stage"] = self.project_time_df[["Project", "Budget Section"]] \
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Merge project_time_df with user_df to populate the role column
        self.project_time_df = merge_dataframes(df=self.project_time_df, merge_data=user_validation, merge_on="Person",
                                                merge_cols=["Person", "Role"])

        # Check if person exists in user data received
        self.project_time_df = isin_check(df=self.project_time_df, validation_df=user_validation,
                                          validation_col="Person", check_cols=["Person"])

        # Rename Person Exists to distinguish data form when calling check_for_placeholders
        self.project_time_df.rename({"Person Exists": "Time - Person Exists"}, axis=1, inplace=True)

        # Check if project exist in project data received
        self.project_time_df = isin_check(df=self.project_time_df, validation_df=stage_validation,
                                          check_cols=["Project"])

        # Check if stage exists against the project in the project data received
        self.project_time_df = isin_check(df=self.project_time_df, validation_df=stage_validation,
                                          validation_col="Stage Validation", check_cols=["Time - Stage"])

        # --------- User Figures --------- #
        # Create the user import dataframes to allow for import of user figures if provided
        self.users_df = create_df.create_import_template(import_columns.USERS_COL)
        self.user_fig_df = create_df.create_import_template(import_columns.USER_FIG_COL)
        self.clash_df = create_df.create_import_template(import_columns.CLASH_COL)
        self.delegate_df = create_df.create_import_template(import_columns.USER_DELEGATES_COL)

        # Map time_user_figs_rec to user figures import sheet
        self.user_fig_df = conv_funcs.remap_columns(df=self.user_fig_df, data=self.time_user_figs_rec,
                                                    mapping_dict=remapping_dicts.TIME_USER_FIG_MAP)

        # Merge user figures with users sheet received to populate role/working hours/productivity if left blank

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="5. Project Time",
                    dataframe_dict={
                        "Timesheets": self.project_time_df,
                        }
                    )

        if len(self.user_fig_df["Person"].tolist()) < 0:
            ExcelWriter(bypass_len_check=True,
                        file_path=file_path,
                        excel_file_name="5. Project Time User Figures",
                        dataframe_dict={
                            "Users": self.users_df,
                            "User Figures": self.user_fig_df,
                            "Time Off Clash Groups": self.clash_df,
                            "User Delegates": self.delegate_df,
                            }
                        )

        # Run checks for placeholder values used
        check_funcs.check_for_placeholders(check_type=error_checks.proj_time_check, df=self.project_time_df,
                                           class_name="Project Time", file_path=file_path)
