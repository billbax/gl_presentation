import pandas as pd


def merge_dataframes(df, merge_data, merge_on, merge_cols, merge_col_dict=None, rename_dict=None):

    # Create a dataframe containing all the relevant information that is to be transferred
    try:
        merge_df = pd.DataFrame()
        for col in merge_cols:
            if merge_col_dict is not None:
                merge_df[col] = merge_data[merge_col_dict[col]]
            else:
                merge_df[col] = merge_data[col]

        # Check if rename_dict variable has been passed if True, rename columns so they can merge
        if rename_dict is not None:
            merge_df.rename(rename_dict, axis=1, inplace=True)

        # Drop duplicates so only the 1st value is passed over
        merge_df.drop_duplicates(subset=merge_on, inplace=True)

        df = df.merge(merge_df[pd.notnull(merge_df[merge_on])], on=merge_on, how="left")
        return df
    except:
        return df.columns([merge_cols])
