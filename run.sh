#!/bin/bash

# Works: Savanna fires for the United States of America.
python src/print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
echo "exit code: $?"

# Works: mean of the same values.
python src/print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv \
    --operation mean
echo "exit code: $?"

# Errors: the data file does not exist.
python src/print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/no_such_file.csv
echo "exit code: $?"

# Errors: "Country" is not a header in the file.
python src/print_fires.py \
    --country "United States of America" \
    --country_column Country \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
echo "exit code: $?"
