# Python Refresher

Command-line tools for pulling emission values out of the Agrifood CO2
emission dataset. `print_fires.py` reports the values of one emission
column, such as savanna fires or forest fires, for a single country
across every year in the dataset. The heavy lifting is done by
`get_column()` in `my_utils.py`, a small reusable utility that returns the
numeric values of one CSV column for the rows where another column matches
a given value.

## Installation

The project depends only on Python and `pycodestyle`. Create the
environment from `environment.yml` and activate it:

```bash
mamba env create -f environment.yml
mamba activate swe4s
```

Check the style of the source with:

```bash
pycodestyle my_utils.py print_fires.py
```

## Data

The program reads a comma-separated file whose first line is a header row.
This project uses `data/Agrofood_co2_emission.csv`, which comes from the
assignment materials and is not committed to the repository. Put it at:

```text
data/Agrofood_co2_emission.csv
```

The file has 31 columns. The first is `Area` (the country) and the second
is `Year`; the rest are emission sources such as `Savanna fires`,
`Forest fires`, and `Crop Residues`. Each row is one country-year.

## Usage

```text
usage: print_fires [-h] --country COUNTRY --country_column COUNTRY_COLUMN
                   --fires_column FIRES_COLUMN --file_name FILE_NAME

Print fire-emission values for one country.

options:
  -h, --help            show this help message and exit
  --country COUNTRY     Country to report on, as it appears in the file
  --country_column COUNTRY_COLUMN
                        Country column, as an index or a header name
  --fires_column FIRES_COLUMN
                        Emission column to print, index or header name
  --file_name FILE_NAME
                        Path to the emissions CSV file
```

All four arguments are required, and their order does not matter. The two
column arguments accept either a zero-based column index or a header name,
so `--fires_column 2` and `--fires_column "Savanna fires"` are equivalent.
Header names containing spaces must be quoted.

### Examples

Savanna fire emissions for the United States, by header name:

```bash
python print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
```

```text
[1391.1481, 1391.1481, 1391.1481, ...]
```

The same query using column indices:

```bash
python print_fires.py \
    --country "United States of America" \
    --country_column 0 \
    --fires_column 2 \
    --file_name data/Agrofood_co2_emission.csv
```

Forest fire emissions for Ghana:

```bash
python print_fires.py \
    --country Ghana \
    --country_column Area \
    --fires_column "Forest fires" \
    --file_name data/Agrofood_co2_emission.csv
```

`run.sh` runs three examples: one that succeeds and two that fail.

```bash
./run.sh
```

### Errors

Errors are reported as a short message and an exit code of 1, with no
traceback. Missing or malformed arguments are caught by argparse and exit
with code 2.

| Situation | Message |
| --- | --- |
| The file does not exist | `Could not find data/no_such_file.csv` |
| The file cannot be read | `Could not read data/Agrofood_co2_emission.csv` |
| The column name is not a header | `Column "Country" is not a header in this file` |
| The column index is out of range | `Column index 999 is out of range for a file with 31 columns` |
| The requested column is not numeric | `Could not convert "Ghana" in column Area to a number` |
| No row matches the country | `No rows matched Atlantis` |

For example, asking for a country column that does not exist:

```bash
python print_fires.py \
    --country "United States of America" \
    --country_column Country \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
```

```text
Column "Country" is not a header in this file
```
