# Python Refresher

Command-line tools for pulling emission values out of the Agrifood CO2
emission dataset. `print_fires.py` reports the values of one emission
column, such as savanna fires or forest fires, for a single country
across every year in the dataset, or optionally their mean, median, or
standard deviation. The heavy lifting is done by `get_column()` in
`src/my_utils.py`, a small reusable utility that returns the numeric values
of one CSV column for the rows where another column matches a given value.

## Changes in 3.0

- `src/my_utils.py` has new `get_mean()`, `get_median()`, and `get_std()`
  functions (standard deviation is the population standard deviation).
- `print_fires.py` takes an optional `--operation` argument (`mean`,
  `median`, or `std`) that prints a summary instead of the raw values.
- Unit tests live in `test/unit/test_my_utils.py` and functional tests in
  `test/func/test_print_fires.sh`, which run against a small, committed
  data file, `test/data/emissions_subset.csv`.
- Source moved to `src/` and tests to `test/`.

## Repository layout

```text
src/                 print_fires.py and my_utils.py
test/unit/           unit tests for my_utils.py (unittest)
test/func/           functional tests for print_fires.py (ssshtest)
test/data/           small data file used by the functional tests
data/                full dataset (not committed)
run.sh               example runs of print_fires.py
```

## Installation

The project depends only on Python and `pycodestyle`. Create the
environment from `environment.yml` and activate it:

```bash
mamba env create -f environment.yml
mamba activate swe4s
```

Check the style of the source with:

```bash
pycodestyle src/*.py test/unit/*.py
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
                   [--operation {mean,median,std}]

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
  --operation {mean,median,std}
                        Summarize the values instead of printing them
```

The first four arguments are required, and their order does not matter. The two
column arguments accept either a zero-based column index or a header name,
so `--fires_column 2` and `--fires_column "Savanna fires"` are equivalent.
Header names containing spaces must be quoted. If `--operation` is given,
a single number (the mean, median, or population standard deviation of the
values) is printed instead of the list.

### Examples

Savanna fire emissions for the United States, by header name:

```bash
python src/print_fires.py \
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
python src/print_fires.py \
    --country "United States of America" \
    --country_column 0 \
    --fires_column 2 \
    --file_name data/Agrofood_co2_emission.csv
```

Forest fire emissions for Ghana:

```bash
python src/print_fires.py \
    --country Ghana \
    --country_column Area \
    --fires_column "Forest fires" \
    --file_name data/Agrofood_co2_emission.csv
```

The mean of the United States savanna fire emissions:

```bash
python src/print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv \
    --operation mean
```

```text
1392.011551612903
```

`run.sh` runs four examples: two that succeed and two that fail.

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
| A matched value is blank | `Could not convert "" in column Savanna fires to a number` |

For example, asking for a country column that does not exist:

```bash
python src/print_fires.py \
    --country "United States of America" \
    --country_column Country \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
```

```text
Column "Country" is not a header in this file
```

## Testing

Run all commands from the repository root with the `swe4s` environment
active.

Unit tests for `my_utils.py` use Python's built-in `unittest`. Each
function is tested with fixed inputs, with randomly generated inputs checked
against Python's `statistics` module, and with inputs that should raise
errors (for example, an empty list):

```bash
python -m unittest discover -s test/unit
```

Functional tests for `print_fires.py` use the
[Stupid Simple Bash Testing](https://github.com/ryanlayer/ssshtest)
framework, which the script downloads with `wget` on its first run. They
check the printed values, each operation, and the exit codes for success
(0), handled errors (1), and argument errors (2):

```bash
bash test/func/test_print_fires.sh
```

The functional tests use `test/data/emissions_subset.csv`, a subset of the
full dataset: five years of Afghanistan (an odd number of values), four
years of Ghana (an even number of values, and negative `Forestland`
values), and two years of Holy See (blank emission values).
