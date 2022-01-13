# 96-Well-Plate-Randomiser
Takes a CSV of 96-well plates and shuffles appends two new columns with a new (randomly chosen) plate and coordinate

## Features
 - Configuration of control wells which should not be randomised

## Requirements
 - You have one or more 96-well plates, you want to randomise the wells inside them to any of the other plates in the same CSV.
 - Well coordinates must be in the format A1 - H12
 - Plate IDs can be any string
 - Before running the script, you must define the variables at the top of the script.

## Running
`python3 ./96-well-plate-randomiser.py`



