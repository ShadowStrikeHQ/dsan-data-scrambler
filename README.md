# dsan-data-scrambler
A command-line utility to randomly shuffle column values within CSV files, ensuring that relationships within a single column are preserved but relationships between columns are broken, thus providing anonymization for data analysis. It takes filename and list of column indices to scramble. - Focused on Tools for anonymizing and de-identifying sensitive data within datasets or text files, focusing on generating realistic fake data while preserving data structure.

## Install
`git clone https://github.com/ShadowStrikeHQ/dsan-data-scrambler`

## Usage
`./dsan-data-scrambler [params]`

## Parameters
- `-h`: Show help message and exit
- `-c`: No description provided
- `-o`: Path to the output CSV file. If not provided, the original file is overwritten.
- `--log-level`: No description provided

## License
Copyright (c) ShadowStrikeHQ
