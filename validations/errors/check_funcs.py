from validations.errors.error_msgs import error_dict
from datetime import datetime

TODAY = datetime.today().strftime("%d.%m.%Y")


def check_for_placeholders(check_type, df, file_path, class_name=""):
    txt_file = open(f"{file_path}/Data Import/{TODAY}/Errors.txt", "a")

    if class_name != "":
        txt_file.write(f"\n\n{class_name}")

    errors = []
    for col in check_type:
        if check_type[col] in df[col].tolist():
            errors += [col]

    for error in errors:
        txt_file.write(f"\n{error_dict[error]}")

    txt_file.close()


def non_config_data(df, system_data, columns, file_path):
    txt_file = open(f"{file_path}/Data Import/{TODAY}/Errors.txt", "a")

    for column in columns:
        config_set = system_data[column].tolist()
        df_set = [item for item in set(df[column].tolist())
                  if item not in ["Non-Chargeable Admin", "Pending", "Pre-CMap"]]

        if any(x not in config_set for x in df_set):
            non_conform_list = [item for item in df_set if item not in config_set]
            txt_file.write(f'\n- {", ".join(non_conform_list)} {error_dict[f"New {column}"]}')

    txt_file.close()
