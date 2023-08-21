import re
import sys
import argparse

def extract_datasets_from_dofile(dofile_path, save_to_file=False):
    with open(dofile_path, 'r') as f:
        content = f.read()

    # Split by exit command if it exists
    parts = content.split('exit', 1)
    analyzed_content = parts[0]

    # Remove all comments (both // and /* */ style)
    analyzed_content = re.sub(r'//.*', '', analyzed_content)
    analyzed_content = re.sub(r'/\*.*?\*/', '', analyzed_content, flags=re.DOTALL)

    # Extract datasets
    entry_datasets = set(re.findall(r'\buse\b\s+(.*?)(?:,|\n)', analyzed_content))
    output_datasets = set(re.findall(r'(?:\bsave\b|\boutsheet\b)\s+(.*?)(?:,|\n)', analyzed_content))
    using_datasets = set(re.findall(r'\busing\b\s+(.*?)(?:,|\n)', analyzed_content))
    temp_datasets = set(re.findall(r'\btempfile\b\s+(.*?)(?:\s|\n)', analyzed_content))

    # Remove outputs from entry if they appear in both
    entry_datasets = entry_datasets - output_datasets

    # Print datasets
    print("Datasets used as entry:")
    for dataset in sorted(entry_datasets):
        print(f"// {dataset}")

    print("\nDatasets produced and reused within the code:")
    reused_datasets = output_datasets.intersection(entry_datasets).union(output_datasets.intersection(using_datasets))
    for dataset in sorted(reused_datasets):
        print(f"// {dataset}")

    print("\nDatasets produced but not reused within the code:")
    not_reused_datasets = output_datasets - reused_datasets
    for dataset in sorted(not_reused_datasets):
        print(f"// {dataset}")

    print("\nTemporary datasets created with 'tempfile':")
    for dataset in sorted(temp_datasets):
        print(f"// '{dataset}'")

    # Save to file if the flag is set
    if save_to_file:
        with open("output_datasets_info.txt", 'w') as f:
            f.write("Datasets used as entry:\n")
            for dataset in sorted(entry_datasets):
                f.write(f"// {dataset}\n")

            f.write("\nDatasets produced and reused within the code:\n")
            for dataset in sorted(reused_datasets):
                f.write(f"// {dataset}\n")

            f.write("\nDatasets produced but not reused within the code:\n")
            for dataset in sorted(not_reused_datasets):
                f.write(f"// {dataset}\n")

            f.write("\nTemporary datasets created with 'tempfile':\n")
            for dataset in sorted(temp_datasets):
                f.write(f"// '{dataset}'\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract datasets from a Stata do-file.")
    parser.add_argument("dofile_path", help="Path to the Stata do-file.")
    parser.add_argument("-s", "--save", help="Save datasets info to an output file.", action="store_true")
    args = parser.parse_args()

    extract_datasets_from_dofile(args.dofile_path, args.save)
