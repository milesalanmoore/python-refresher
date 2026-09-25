#!/bin/bash
# Functional tests for print_fires.py using the Stupid Simple Bash Testing
# framework (https://github.com/ryanlayer/ssshtest).
#
# Run from anywhere with: bash test/func/test_print_fires.sh

test_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$test_dir" || exit 1

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

print_fires=../../src/print_fires.py
data=../data/emissions_subset.csv

# Without an operation, the values are printed in file order.
run test_values_by_name python $print_fires \
    --country Afghanistan \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data
assert_exit_code 0
assert_stdout
assert_in_stdout "[38.9302, 30.9378, 64.1411, 46.1683, 22.781]"

run test_values_by_index python $print_fires \
    --country Ghana \
    --country_column 0 \
    --fires_column 3 \
    --file_name $data
assert_exit_code 0
assert_in_stdout "[169.7846, 577.4328, 1499.1857, 837.7871]"

run test_negative_values python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column Forestland \
    --file_name $data \
    --operation mean
assert_exit_code 0
assert_in_stdout "-13821.5288"

# Operations on an odd number of values (Afghanistan, 5 rows).
run test_mean_odd python $print_fires \
    --country Afghanistan \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation mean
assert_exit_code 0
assert_in_stdout "40.59168"
assert_no_stderr

run test_median_odd python $print_fires \
    --country Afghanistan \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation median
assert_exit_code 0
assert_in_stdout "38.9302"

run test_std_odd python $print_fires \
    --country Afghanistan \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation std
assert_exit_code 0
assert_in_stdout "14.13401648"

# Operations on an even number of values (Ghana, 4 rows).
run test_mean_even python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation mean
assert_exit_code 0
assert_in_stdout "4283.68845"

run test_median_even python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation median
assert_exit_code 0
assert_in_stdout "4080.57975"

run test_std_even python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation std
assert_exit_code 0
assert_in_stdout "479.50501967"

# Errors handled by print_fires.py exit with code 1 and a short message.
run test_missing_file python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name ../data/no_such_file.csv
assert_exit_code 1
assert_in_stdout "Could not find ../data/no_such_file.csv"
assert_no_stderr

run test_unknown_column_name python $print_fires \
    --country Ghana \
    --country_column Country \
    --fires_column "Savanna fires" \
    --file_name $data
assert_exit_code 1
assert_in_stdout 'Column "Country" is not a header in this file'

run test_column_index_out_of_range python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column 999 \
    --file_name $data
assert_exit_code 1
assert_in_stdout "Column index 999 is out of range"

run test_non_numeric_column python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column Area \
    --file_name $data
assert_exit_code 1
assert_in_stdout 'Could not convert "Ghana" in column Area to a number'

run test_blank_value python $print_fires \
    --country "Holy See" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation mean
assert_exit_code 1
assert_in_stdout 'Could not convert "" in column Savanna fires to a number'

run test_no_matching_rows python $print_fires \
    --country Atlantis \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation median
assert_exit_code 1
assert_in_stdout "No rows matched Atlantis"

# Errors caught by argparse exit with code 2.
run test_unknown_operation python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name $data \
    --operation mode
assert_exit_code 2
assert_in_stderr "invalid choice: 'mode'"
assert_no_stdout

run test_missing_argument python $print_fires \
    --country Ghana \
    --country_column Area \
    --fires_column "Savanna fires"
assert_exit_code 2
assert_in_stderr "the following arguments are required: --file_name"
