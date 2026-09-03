# Python Refresher

This repository contains the completed work for Assignment 1: Git and Python
for Software Engineering for Scientists.

## Changes

- Implemented the `get_column()` function in `my_utils.py`.
- Added support for identifying columns by numeric index or column name.
- Added the named `result_column` argument, which defaults to column `1`.
- Updated `print_fires.py` to use `get_column()` and print fire-emission values
  for the United States of America.
- Added `run.sh` to execute `print_fires.py`.

## Data File

The program requires the following data file:

```text
data/Agrofood_co2_emission.csv

This file must be obtained from the assignment materials. It is intentionally
not committed to the repository, as required by the assignment instructions.

Usage

Run the program directly with Python:

python3 print_fires.py

Alternatively, run it using the shell script:

./run.sh
```
