# Please read the README.md file for more information.

################################################################################
# Filename to load the 96 well plate data from *THIS WILL NOT BE MODIFIED*
csv_input = "input.csv"

# Filename to save the data from input.csv with the additional column of randomised coordinates
csv_output = "output.csv"

# Filename to save the sorted data to a CSV file
csv_sorted = "sorted.csv"

# Set to True if the CSV has a header row, False if not
csv_has_header = True

# Column number of the plate ID in the CSV (starting at 0)
csv_plate_id_column = 5

# Column number of the well coordinates in the CSV (starting at 0)
csv_well_column = 6

# Control (plate, well) tuples which should not be moved (if empty, all wells will be moved)
control_wells = [("78500", "A1"), ("BB143_plate07", "A12"), ("BB143_plate15", "H12")]

# Number of plates (for sanity checking)
number_of_plates = 3

# How many times should the randomisation be performed? Doesn't really make a difference, but it's here if you want to.
number_of_randomisations = 100

# If the value in this column ID is empty, then consider the row as an empty row and skip it
empty_column_id = 0

# Rename plates in order of appearance in the CSV, if empty then no renaming will be done
rename_plates = ["final_1", "final_2", "final_3"]

################################################################################

import csv
import random

# Well Plate Layout
letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Custom sorting function to sort the wells A1-H12 in the order A1, A2, ..., H12
def sort_wells(well_a, well_b):
    if letters.index(well_a[0]) < letters.index(well_b[0]):
        return -1
    elif letters.index(well_a[0]) > letters.index(well_b[0]):
        return 1
    elif numbers.index(int(well_a[1])) < numbers.index(int(well_b[1])):
        return -1
    elif numbers.index(int(well_a[1])) > numbers.index(int(well_b[1])):
        return 1
    else:
        return 0


# Get a list of all plates in the CSV
plates = []
with open(csv_input, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    if csv_has_header:
        next(csv_reader)
    for row in csv_reader:
        if row[csv_plate_id_column] not in plates:
            plates.append(str(row[csv_plate_id_column]))

# Check that the number of plates to be renamed matches the number of plates found in the CSV, if 'rename_plates' is not empty
if len(rename_plates) > 0 and len(rename_plates) != len(plates):
    print(
        "ERROR: The number of plates to be renamed does not match the number of plates found in the CSV!"
    )
    exit()

# If there are not exactly the correct number of unique plates found, we have a problem.
if len(plates) != number_of_plates:
    print(
        "ERROR: Unexpected number of plates found in CSV. Expected "
        + str(number_of_plates)
        + " but found "
        + str(len(plates))
        + "."
    )
    exit()


# If we are renaming plates, then we need to override the new plate names
if len(rename_plates) > 0:
    generate_plates = rename_plates
else:
    generate_plates = plates


# Build a list of tuples of all possible coordinates for each plate
wells = []
for plate in generate_plates:
    for number in numbers:
        for letter in letters:
            wells.append((str(plate), letter + str(number)))

# Remove any control wells from the wells list, taking into account the rename_plates override
for control_plate, control_well in control_wells:
    if len(rename_plates) > 0:
        control_plate = rename_plates[plates.index(control_plate)]
    wells.remove((control_plate, control_well))


with open(csv_input, "r") as csv_file:
    with open(csv_output, "w") as csv_output_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(csv_output_file)

        # Count how many columns are in the CSV
        column_count = 0
        for row in csv_reader:
            column_count = len(row)

        # Rewind the file
        csv_file.seek(0)

        # If the CSV has a header, add two columns to the end and add it to the output CSV
        if csv_has_header:
            csv_writer.writerow(next(csv_reader) + ["output_plate", "output_well"])

        # Count the number of rows in the CSV
        row_count = 0
        for row in csv_reader:
            row_count += 1

        # Reset the CSV file to the start, line 1 if there is a header
        csv_file.seek(0)
        if csv_has_header:
            next(csv_reader)

        # If the number of available wells is smaller than the number of rows, we have a problem.
        if len(wells) < row_count:
            print(
                "ERROR: Unexpected number of available wells. Need at least "
                + str(row_count)
                + " but found "
                + str(len(wells))
                + "."
            )
            exit()

        # Slice the wells var to the number of rows we have
        wells = wells[:row_count]

        # Shuffle the wells 'number_of_randomisation' times
        for i in range(number_of_randomisations):
            random.shuffle(wells)

        # Loop through the input CSV and add the new columns to the output CSV
        for row in csv_reader:
            if (row[csv_plate_id_column], row[csv_well_column]) not in control_wells:
                next_well = wells.pop()
                row.extend([next_well[0], next_well[1]])
                csv_writer.writerow(row)
            else:

                # Find the new renamed plate based on the original plate name
                if len(rename_plates) > 0:
                    for i in range(len(plates)):
                        if row[csv_plate_id_column] == plates[i]:
                            plate_name = rename_plates[i]
                else:
                    plate_name = row[csv_plate_id_column]

                row.extend([plate_name, row[csv_well_column]])
                csv_writer.writerow(row)


# Sort the output.csv file by the output_plate and output_well columns
with open(csv_output, "r") as csv_file:
    with open(csv_sorted, "w") as csv_output_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(csv_output_file)

        # If the CSV has a header, print it as it is
        if csv_has_header:
            csv_writer.writerow(next(csv_reader))

        # Sort the rows by the output_plate and output_well columns with natural sorting
        for row in sorted(
            csv_reader,
            key=lambda x: (
                x[column_count],
                x[column_count + 1][:1],
                int(x[column_count + 1][1:]),
            ),
        ):
            csv_writer.writerow(row)
