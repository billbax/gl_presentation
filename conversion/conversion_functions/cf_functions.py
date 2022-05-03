import conversion.conversion_functions.create_dataframes as create_df


def custom_field_check(standard_cols, data, len_check):
    # Create an empty dataframe for the custom fields to be added to
    custom_field_df = create_df.create_import_template(columns=[])

    # Create a list of the identifier/custom columns
    custom_fields = [item for item in list(data.columns.values) if item not in standard_cols]

    # If more items in list than identifier columns populate the dataframe with the data
    if len(custom_fields) > len_check:
        for field in custom_fields:
            custom_field_df[field] = data[field]

    return custom_field_df
