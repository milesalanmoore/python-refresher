"""Print the values of a fire-emission column for one country.

Reads a CSV of agrifood CO2 emissions and prints the values of the
requested emission column for every row matching the requested country.
"""
import argparse
import sys

import my_utils


def parse_column(value):
    """Parse a command-line column as an index if numeric, else a name.

    Parameters
    ----------
    value : str
        Column as given on the command line.

    Returns
    -------
    int or str
        The column as a zero-based index, or as a header name.
    """
    try:
        return int(value)
    except ValueError:
        return value


def get_args():
    """Parse the command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments: country, country_column, fires_column, file_name.
    """
    parser = argparse.ArgumentParser(
        description='Print fire-emission values for one country.',
        prog='print_fires')
    parser.add_argument('--country',
                        type=str,
                        help='Country to report on, as it appears in the file',
                        required=True)
    parser.add_argument('--country_column',
                        type=parse_column,
                        help='Country column, as an index or a header name',
                        required=True)
    parser.add_argument('--fires_column',
                        type=parse_column,
                        help='Emission column to print, index or header name',
                        required=True)
    parser.add_argument('--file_name',
                        type=str,
                        help='Path to the emissions CSV file',
                        required=True)
    return parser.parse_args()


def main():
    """Print the requested column, or report the error and exit non-zero."""
    args = get_args()

    try:
        fires = my_utils.get_column(args.file_name,
                                    args.country_column,
                                    args.country,
                                    result_column=args.fires_column)
    except FileNotFoundError:
        print('Could not find ' + args.file_name)
        sys.exit(1)
    except PermissionError:
        print('Could not read ' + args.file_name)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if not fires:
        print('No rows matched ' + args.country)
        sys.exit(1)

    print(fires)


if __name__ == '__main__':
    main()
