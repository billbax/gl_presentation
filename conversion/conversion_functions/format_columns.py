
def remap_columns(df, data, mapping_dict):
    for mapping in mapping_dict:
        try:
            df[mapping] = data[mapping_dict[mapping]]
        except KeyError:
            # print(f"{mapping} not found.")
            pass
    return df


def fill_columns(df, fill_column_dict):
    for col in fill_column_dict:
        try:
            df[col].fillna((fill_column_dict[col]), inplace=True)
        except KeyError:
            pass

    return df
