import conversion.conversion_defaults.import_tool_columns as import_columns
import conversion.conversion_defaults.remapping_dicts as remapping_dicts
import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from conversion.conversion_functions.merge_dataframes import merge_dataframes
from excel_writer.excel_writer_class import ExcelWriter
import validations.errors.check_funcs as check_funcs
from validations.errors import error_checks

CMAP_PLACEHOLDERS = ["1000 (Cmap)", "1001 (Cmap)", "1002 (Cmap)"]


class ProjectFees:
    def __init__(self, client_data, project_validation, file_path):
        # Create the fee estimator dataframes required by the import tool from the lists of default columns
        self.fe_top_lvl_df = create_df.create_import_template(import_columns.FE_COL)
        self.fe_tab_df = create_df.create_import_template(import_columns.FE_TAB_COL)
        self.fe_section_df = create_df.create_import_template(import_columns.FE_SECT_COL)
        self.fe_task_df = create_df.create_import_template(import_columns.FE_TASK_COL)
        self.fe_externals_df = create_df.create_import_template(import_columns.FE_EXT_COL)

        # Extract the fee estimator data from the client data sheet received
        self.fee_data_received = create_df.read_sheet(data=client_data, sheet_name="Top Down Project Fees")
        self.externals_data_received = create_df.read_sheet(data=client_data, sheet_name="Additionals")

        # Remove all CMap example rows based on (Cmap) cell identifier
        self.fee_data_received = create_df.remove_placeholders(data=self.fee_data_received, column_header="Project Number",
                                                               placeholders=CMAP_PLACEHOLDERS)
        self.external_data_received = create_df.remove_placeholders(data=self.externals_data_received, column_header="project Number",
                                                                    placeholders=CMAP_PLACEHOLDERS)

        # Remap the columns received into the dataframes for import using the dicts in remapping_dict
        self.fe_top_lvl_df = conv_funcs.remap_columns(df=self.fe_top_lvl_df, data=self.fee_data_received,
                                                      mapping_dict=remapping_dicts.FE_FEE_EST_MAP)
        self.fe_tab_df = conv_funcs.remap_columns(df=self.fe_tab_df, data=self.fee_data_received,
                                                  mapping_dict=remapping_dicts.FE_TAB_MAP)
        self.fe_section_df = conv_funcs.remap_columns(df=self.fe_section_df, data=self.fee_data_received,
                                                      mapping_dict=remapping_dicts.FE_SECTION_MAP)
        self.fe_task_df = conv_funcs.remap_columns(df=self.fe_task_df, data=self.fee_data_received,
                                                   mapping_dict=remapping_dicts.FE_TASKS_MAP)
        self.fe_externals_df = conv_funcs.remap_columns(df=self.fe_externals_df, data=self.externals_data_received,
                                                        mapping_dict=remapping_dicts.FE_EXT_MAP)

        # Remove duplicate values from fe_top_lvl_df & fe_tab_df
        self.fe_top_lvl_df.drop_duplicates(subset="Project", inplace=True)
        self.fe_tab_df.drop_duplicates(subset="Project", inplace=True)

        # Merge fe_top_lvl_df with proj_det

        # Merge fe_section_df with proj_det_df to populate the 'Status' column
        self.fe_section_df = merge_dataframes(df=self.fe_section_df, merge_data=project_validation.proj_det_df,
                                              merge_on="Project", rename_dict={"Code": "Project"},
                                              merge_cols=["Code", "Status"])

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.fe_top_lvl_df = conv_funcs.fill_columns(df=self.fe_top_lvl_df, fill_column_dict=fill_columns.NULL_FE_TOP)
        self.fe_tab_df = conv_funcs.fill_columns(df=self.fe_tab_df, fill_column_dict=fill_columns.NULL_FE_TAB)
        self.fe_section_df = conv_funcs.fill_columns(df=self.fe_section_df, fill_column_dict=fill_columns.NULL_FE_SECT)
        self.fe_task_df = conv_funcs.fill_columns(df=self.fe_task_df, fill_column_dict=fill_columns.NULL_FE_TASK)
        self.fe_externals_df = conv_funcs.fill_columns(df=self.fe_externals_df, fill_column_dict=fill_columns.NULL_FE_EXT)

        # Convert duration from weeks to days
        self.fe_task_df["Duration"] = self.fe_task_df["Duration"] * 7

        # Concatenate project/stage to create a 'Stage Validation' column to allow validation/merges in other classes
        self.fe_section_df["Stage Validation"] = self.fe_section_df[["Project", "Section Name"]] \
            .apply(lambda row: " ".join(row.values.astype(str)), axis=1)

        # Rename 'Bid Stage' stage type to 'Y' to be accepted by import tool
        self.fe_section_df["Stage Type"].replace({"Y": "Bid Stage"}, inplace=True)

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="11. Fee Estimator",
                    dataframe_dict={
                        "Fee Estimator": self.fe_top_lvl_df,
                        "Fee Estimator Tabs": self.fe_tab_df,
                        "Fee Estimator Sections": self.fe_section_df,
                        "Fee Estimator Tasks": self.fe_task_df,
                        "Fee Estimator Externals": self.fe_externals_df,
                        }
                    )

        # Run checks for placeholder values/non config internal codes used
        check_funcs.check_for_placeholders(check_type=error_checks.fee_estimator_check, df=self.fe_task_df,
                                           class_name="Fee Estimator", file_path=file_path)
