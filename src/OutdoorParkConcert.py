"""
This example code creates a 2d list (2d matrix) that can store seating.
The matrix is populated with . since all seats are available
"""

# our test matrix has 4 rows and 10 columns
N_ROW = 4
N_COL = 10

# available seat
available_seat = '.'

# create some available seating
seating = []
for r in range(N_ROW):
    row = []
    for c in range(N_COL):
        row.append(available_seat)
    seating.append(row)

# print available seating
for r in range(N_ROW):
    print(r+1, end="\t")
    for c in range(N_COL):
        print(seating[r][c], end=" ")
    print()
