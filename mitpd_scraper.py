import tabula

test_files = [
    "example_data1.pdf",
    "example_data2.pdf",
    "example_data3.pdf"
]

file = "example_data.pdf"
# tables_3 = tabula.read_pdf(file, pages = "all", multiple_tables = True, pandas_options={'header': None})
tables = []

for file in test_files:
    tables.append(tabula.read_pdf(file, pages = "all", multiple_tables = True, \
        pandas_options={'header': None}, stream=True, guess=True, \
        area=(140, 0, 605, 790))[0])

for t in tables:
    print(t)
    print()
    print()



# coords (40, 140), (780, 140), (40, 310), (780, 310) area=(140, 40, 605, 780)
# columns x 133, 200, 293, 415, 716