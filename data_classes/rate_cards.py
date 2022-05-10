import conversion.conversion_defaults.fill_columns as fill_columns
import conversion.conversion_functions.format_columns as conv_funcs
import conversion.conversion_functions.create_dataframes as create_df
from excel_writer.excel_writer_class import ExcelWriter

CMAP_PLACEHOLDERS = ["CMap Specific Rate (Cmap)", "Standard Rate Card (Cmap)"]


class RateCards:
    def __init__(self, client_data, file_path):
        # Extract the rates data from the client data sheet received
        self.rates_rec = create_df.read_sheet(data=client_data, sheet_name="Rate Cards")

        # Remove all CMap example rows based on (cmap) cell identifier
        self.rates_rec = create_df.remove_placeholders(data=self.rates_rec, column_header="Rate Card Name",
                                                       placeholders=CMAP_PLACEHOLDERS)

        # Pivot role information into required format
        self.rates_rec = self.rates_rec.melt(id_vars=("Rate Card Name", "Standard Rate", "Currency"),
                                             var_name="Role", value_name="Charge Rate")

        # Add additional mandatory fields required by import tool
        self.rates_df = self.rates_rec.reindex(columns=self.rates_rec.columns.tolist() +
                                               ["Cost Rate", "Live", "Office", "Team", "Order Number"])

        # Fill any null mandatory columns using the placeholder dict from fill_columns
        self.rates_df = conv_funcs.fill_columns(df=self.rates_df, fill_column_dict=fill_columns.NULL_RATES)

        # Export dataframes to excel
        ExcelWriter(file_path=file_path,
                    excel_file_name="4. Rate Cards",
                    dataframe_dict={
                        "Budget Rates": self.rates_df,
                        }
                    )
