# Please read the README.md file for more information.

################################################################################
# Filename to load the 96 well plate data from *THIS WILL NOT BE MODIFIED*
csv_input = "input.csv"

# Filename to save the data from input.csv with the additional column of randomised coordinates
csv_output = "output.csv"

# Set to True if the CSV has a header row, False if not
csv_has_header = True

# Column number of the plate ID in the CSV (starting at 0)
csv_plate_id_column = 5

# Column number of the well coordinates in the CSV (starting at 0)
csv_well_column = 6

# Control (plate, well) tuples which should not be moved (if empty, all wells will be moved)
control_wells = [("1", "A1"), ("2", "A1"), ("3", "A1")]
################################################################################

import csv
import random
from shutil import copyfile

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Get a list of all plates in the CSV
plates = []
with open(csv_input, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    if csv_has_header:
        next(csv_reader)
    for row in csv_reader:
        if row[csv_plate_id_column] not in plates:
            plates.append(row[csv_plate_id_column])

# If there are not exactly three unique plates found, we have a problem.
if len(plates) != 3:
    print("ERROR: There are not exactly three unique plates in the CSV.")
    exit()

# Build a list of all wells
wells = []
for plate in plates:
    for letter in letters:
        for number in numbers:
            wells.append((plate, letter + str(number)))

# Remove any control wells from the list
for control_plate, control_well in control_wells:
    for well in wells:
        if well[0] == control_plate and well[1] == control_well:
            wells.remove(well)

# Randomise the list of wells
random.shuffle(wells)

# Iterate through the CSV rows, if the well is not a control well, append a new row with the new coordinates
with open(csv_input, "r") as csv_file:
    with open(csv_output, "w") as csv_output_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(csv_output_file)
        # If the CSV has a header, add two columns to the end and add it to the output CSV
        if csv_has_header:
            csv_writer.writerow(next(csv_reader) + ["output_plate", "output_well"])

        # Iterate through the CSV rows
        for row in csv_reader:
            if (row[csv_plate_id_column], row[csv_well_column]) not in control_wells:
                next_well = wells.pop()
                row.extend([next_well[0], next_well[1]])
                csv_writer.writerow(row)
            else:
                row.extend([row[csv_plate_id_column], row[csv_well_column]])
                csv_writer.writerow(row)
