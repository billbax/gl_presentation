def colour_cells(x, values_to_colour, values_to_highlight):
    """Colour text red if a placeholder needed or colour background red if a mandatory field has been left null"""
    if x in values_to_colour:
        color = "color:red"
    elif x in values_to_highlight:
        color = "background-color:red"
    else:
        color = ""
    return color
