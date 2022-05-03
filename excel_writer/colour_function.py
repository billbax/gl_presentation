

def colour_cells(x, values_to_colour, values_to_highlight):
    if x in values_to_colour:
        colour = "color:red"
    elif x in values_to_highlight:
        colour = "background-color:red"
    else:
        colour = ""
    return colour
