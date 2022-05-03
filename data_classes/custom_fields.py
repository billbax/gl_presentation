import conversion.conversion_functions.create_dataframes as create_df
from conversion.conversion_functions.cf_functions import custom_field_check


class CustomFields:
    def __init__(self, client_data,  standard_cols, len_check):
        # Open the client data received
        self.cf_data = client_data

        # Drop all columns in which no column header is given
        self.cf_data.drop(self.cf_data.columns[self.cf_data.columns.str.contains("unnamed", case=False)],
                          axis=1, inplace=True)

        # Check if any custom fields present and populate a dataframe if True else return empty dataframe.
        # Standard cols == All non identifier columns. project number, company name etc are not included as needed for import of custom fields.
        # len_check is the number of identifier columns within the data. Dataframe only created if non identifier columns present
        self.cf_df = custom_field_check(standard_cols=standard_cols, data=self.cf_data, len_check=len_check)
