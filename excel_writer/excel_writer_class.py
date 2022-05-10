import pandas as pd
import os
from datetime import datetime
from excel_writer.colour_function import colour_cells
from excel_writer.styling_dicts import colour_dict, highlight_dict

TODAY = datetime.today().strftime("%d.%m.%Y")


class ExcelWriter:
    def __init__(self, file_path, excel_file_name, dataframe_dict):
        # Create a new directory and name it the current date
        try:
            os.makedirs(f"{file_path}/Data Import/{TODAY}")
        except FileExistsError:
            pass

        # Check if len of dataset is greater than 1. If False return
        if len(list(dataframe_dict.items())[0][1]):
            # Create excel writer in append mode if possible else create a new excel file
            try:
                excel_writer = pd.ExcelWriter(f"{file_path}/Data Import/{TODAY}/{excel_file_name}.xlsx", engine="openpyxl", mode="a")
            except FileNotFoundError:
                excel_writer = pd.ExcelWriter(f"{file_path}/Data Import/{TODAY}/{excel_file_name}.xlsx", engine="openpyxl", mode="w")

            # Add the dataframes from dataframe_dict to the excel writer.
            # If placeholders/warnings in place add colouring else use standard to_excel
            for sheet_name in dataframe_dict:
                try:
                    dataframe_dict[sheet_name].style.applymap(func=colour_cells,
                                                              values_to_colour=colour_dict[sheet_name],
                                                              values_to_highlight=highlight_dict[sheet_name])\
                                                              .to_excel(excel_writer, sheet_name, index=False)
                except KeyError:
                    dataframe_dict[sheet_name].to_excel(excel_writer, sheet_name, index=False)

            # Save the writer
            excel_writer.save()
