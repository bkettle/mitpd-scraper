import fitz
import tabula
import numpy as np
import argparse
import datetime

FILENAME = "example_data1.pdf"

def scrape_log(filename):
    doc = fitz.open(filename)
    page = doc[0]
    doc = fitz.open(filename)
    page = doc[0]

    # a list of thetext to search for to identify each column
    column_text = [
        "Date & Time Reported",
        "Inc Type",
        "Date & Time Occurred",
        "Address",
        "Comments",
        "Disposition"
    ]

    ############
    ## Find table bounding box
    ############

    col_x_offsets = []
    for col_num, text in enumerate(column_text):
        col_x_offsets.append(page.searchFor(text)[0].x0 - 3)
    table_left_x = col_x_offsets[0]

    top_left_text = "Date & Time Reported"
    table_top_y = page.searchFor(top_left_text)[0].y0

    bottom_text = "NO REPORTS OF RESIDENTIAL FIRES"
    table_bottom_y = page.searchFor(bottom_text)[0].y0

    table_right_x = page.searchFor(column_text[-1])[0].x1 + 3

    print("column x offsets", col_x_offsets)

    print(f"table corners: ({table_left_x}, {table_top_y}), ({table_right_x}, {table_bottom_y})")
    table_bounding_box = (table_top_y, table_left_x, table_bottom_y, table_right_x)

    #########
    ## Parse Table
    #########

    table = tabula.read_pdf(FILENAME, pages = "all", multiple_tables = True, \
            pandas_options={'header': None}, stream=True, guess=False, \
            area=table_bounding_box, columns=col_x_offsets, silent=True)[0]

    print(table)

    ##############
    ## Convert messy output to entries
    ##############

    entries = []
    current_entry = None
    for _, row in table.iterrows():
        row = list(row)
        if row[-1] == "OPEN":
            if current_entry:
                entries.append(current_entry)
            # start of an entry, next 2-3 rows will be that entry
            # until the next OPEN
            current_entry = {col: "" for col in column_text}
        # once we find the first row, look at each piece
        if current_entry is not None:
            for col_i, val in enumerate(row):
                # skip first column of nothing (?)
                if col_i == 0:
                    continue
                col_name = column_text[col_i-1]

                if val and val is not np.nan:
                    current_entry[col_name] += str(val) + " "

    if current_entry:
        entries.append(current_entry)

    # clean up output
    for entry in entries:
        for key, val in entry.items():
            entry[key] = val.strip()

    print(entries)

    #############
    ## format to nice strings
    #############

    for entry in entries:
        print(f"On {entry['Date & Time Occurred']} near {entry['Address']}: {entry['Comments']}")
    # a list of thetext to search for to identify each column
    column_text = [
        "Date & Time Reported",
        "Inc Type",
        "Date & Time Occurred",
        "Address",
        "Comments",
        "Disposition"
    ]

    ############
    ## Find table bounding box
    ############

    col_x_offsets = []
    for col_num, text in enumerate(column_text):
        col_x_offsets.append(page.searchFor(text)[0].x0 - 3)
    table_left_x = col_x_offsets[0]

    top_left_text = "Date & Time Reported"
    table_top_y = page.searchFor(top_left_text)[0].y0

    bottom_text = "NO REPORTS OF RESIDENTIAL FIRES"
    table_bottom_y = page.searchFor(bottom_text)[0].y0

    table_right_x = page.searchFor(column_text[-1])[0].x1 + 3

    print("column x offsets", col_x_offsets)

    print(f"table corners: ({table_left_x}, {table_top_y}), ({table_right_x}, {table_bottom_y})")
    table_bounding_box = (table_top_y, table_left_x, table_bottom_y, table_right_x)

    #########
    ## Parse Table
    #########

    table = tabula.read_pdf(FILENAME, pages = "all", multiple_tables = True, \
            pandas_options={'header': None}, stream=True, guess=False, \
            area=table_bounding_box, columns=col_x_offsets, silent=True)[0]

    print(table)

    ##############
    ## Convert messy output to entries
    ##############

    entries = []
    current_entry = None
    for _, row in table.iterrows():
        row = list(row)
        if row[-1] == "OPEN":
            if current_entry:
                entries.append(current_entry)
            # start of an entry, next 2-3 rows will be that entry
            # until the next OPEN
            current_entry = {col: "" for col in column_text}
        # once we find the first row, look at each piece
        if current_entry is not None:
            for col_i, val in enumerate(row):
                # skip first column of nothing (?)
                if col_i == 0:
                    continue
                col_name = column_text[col_i-1]

                if val and val is not np.nan:
                    current_entry[col_name] += str(val) + " "

    if current_entry:
        entries.append(current_entry)

    # clean up output
    for entry in entries:
        for key, val in entry.items():
            entry[key] = val.strip()

    print(entries)

    #############
    ## format to nice strings
    #############

    for entry in entries:
        print(f"On {entry['Date & Time Occurred']} near {entry['Address']}: {entry['Comments']}")

scrape_log(FILENAME)