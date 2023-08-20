# Stata Datasets Extractor

A Python script that processes Stata do-files to extract dataset information, categorizing them into three distinct categories: entry datasets, produced and reused datasets, and produced but not reused datasets. This can be useful in understanding and documenting the flow and manipulation of datasets in complex Stata projects.

## Features
- Extracts dataset names used as entry in the Stata do-file.
- Identifies datasets that are produced and reused within the do-file.
- Identifies datasets that are produced but not reused within the same do-file.
- Options to display dataset information in the terminal and/or save it to a file.
- Ignores datasets and `exit` commands mentioned within comments.

## Requirements
- Python 3

## Usage

1. Clone the repository:
```bash
git clone https://github.com/ChristopheCahn/stata_datasets_extractor.git
cd stata_datasets_extractor
```

2. Run the script:
- To display dataset information in the terminal:
```bash
python3 extract_datasets.py <path_to_stata_dofile.do>
```

- To display dataset information in the terminal and save it to a file:
```bash
python3 extract_datasets.py -s <path_to_stata_dofile.do>
```

## Contribution
Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License
This project is open source, under the [MIT License](LICENSE).
