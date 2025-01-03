import argparse
import logging
import pandas as pd
import random
import os
from typing import List


def setup_argparse() -> argparse.ArgumentParser:
    """Sets up the command line argument parser.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(
        description="Randomly shuffles column values within a CSV file."
    )
    parser.add_argument(
        "filename", type=str, help="Path to the CSV file to process."
    )
    parser.add_argument(
        "-c",
        "--columns",
        type=str,
        required=True,
        help="Comma-separated list of column indices to scramble (e.g., 0,2,4).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output CSV file. If not provided, the original file is overwritten.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO).",
    )
    return parser


def validate_input(filename: str, columns: List[int]) -> None:
    """Validates the input arguments.

    Args:
        filename (str): The path to the CSV file.
        columns (List[int]): The list of column indices.

    Raises:
        FileNotFoundError: If the filename does not point to a valid file.
        ValueError: If there are issues with column indices.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    if not columns:
        raise ValueError("No columns provided to scramble.")

    try:
        df = pd.read_csv(filename)
        num_columns = len(df.columns)
        for col in columns:
            if col < 0 or col >= num_columns:
                raise ValueError(
                    f"Column index {col} is out of range for file {filename}."
                )
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {filename}")
    except Exception as e:
        raise ValueError(f"Error validating file or columns. Details {e}")


def scramble_columns(filename: str, columns: List[int]) -> pd.DataFrame:
    """Scrambles the specified columns of a CSV file.

    Args:
        filename (str): Path to the CSV file.
        columns (List[int]): List of column indices to scramble.

    Returns:
        pd.DataFrame: The modified DataFrame.
    """
    try:
        df = pd.read_csv(filename)
        for col_index in columns:
            col_name = df.columns[col_index]
            col_values = df[col_name].tolist()
            random.shuffle(col_values)
            df[col_name] = col_values
        return df
    except Exception as e:
        logging.error(f"Error during scrambling: {e}")
        raise


def main() -> None:
    """Main function to execute the data scrambling."""
    parser = setup_argparse()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    try:
        columns_indices = [int(c) for c in args.columns.split(",")]
        validate_input(args.filename, columns_indices)

        logging.info(f"Starting scrambling of columns {columns_indices} in {args.filename}")

        modified_df = scramble_columns(args.filename, columns_indices)

        output_file = args.output if args.output else args.filename
        modified_df.to_csv(output_file, index=False)
        logging.info(f"Scrambled data saved to {output_file}")

    except FileNotFoundError as e:
        logging.error(f"File error: {e}")
    except ValueError as e:
        logging.error(f"Input error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Usage Examples:
    # 1. Scramble columns 0 and 2 in data.csv, save output to output.csv
    #   python main.py data.csv -c 0,2 -o output.csv
    # 2. Scramble column 1 in data.csv, overwrite the original file
    #   python main.py data.csv -c 1
    # 3. Scramble columns 0, 1, 2, and 3 with debug logging
    #   python main.py data.csv -c 0,1,2,3 --log-level DEBUG

    main()