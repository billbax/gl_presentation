
def isin_check(df, validation_df, check_cols, validation_col=None):
    """Return Yes or No based on if the value exists within the specified dataset.
     Validation col only required if col in validation df != col in main df"""

    # iterate through each column in check_cols and create a new {col} exists column in main df
    for col in check_cols:
        try:
            df[f"{col} Exists"] = df[col].isin(validation_df[validation_col])
        # if validation col not set, lookup col from for loop in validation df
        except KeyError:
            print(f"isin_check KeyError for {col}")
            df[f"{col} Exists"] = df[col].isin(validation_df[col])

        # Replace boolean values with yes/no
        df[f"{col} Exists"].replace({False: "No", True: 'Yes'}, inplace=True)
    return df
