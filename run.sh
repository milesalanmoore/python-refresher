#!/bin/bash

# Works: Savanna fires for the United States of America.
python print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
echo "exit code: $?"

# Errors: the data file does not exist.
python print_fires.py \
    --country "United States of America" \
    --country_column Area \
    --fires_column "Savanna fires" \
    --file_name data/no_such_file.csv
echo "exit code: $?"

# Errors: "Country" is not a header in the file.
python print_fires.py \
    --country "United States of America" \
    --country_column Country \
    --fires_column "Savanna fires" \
    --file_name data/Agrofood_co2_emission.csv
echo "exit code: $?"
