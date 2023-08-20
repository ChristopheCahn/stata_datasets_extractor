import re
import sys
import argparse

def remove_comments(content):
    # Remove block comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Remove line comments starting with *
    content = re.sub(r'^\*.*?$', '', content, flags=re.MULTILINE)

    # Remove single line comments starting with //
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)

    return content

def truncate_after_exit(content):
    content_no_comments = remove_comments(content)
    exit_position = content_no_comments.find('exit')
    if exit_position != -1:
        content = content[:content.find('exit')]
    return content

def extract_datasets(dofile, save_to_file):
    with open(dofile, 'r') as file:
        content = file.read()

    content = truncate_after_exit(content)
    content_no_comments = remove_comments(content)

    use_pattern = re.compile(r'\buse ([^\s,]+)', re.IGNORECASE)
    save_pattern = re.compile(r'\bsave ([^\s,]+)', re.IGNORECASE)
    using_pattern = re.compile(r'\busing ([^\s,]+)', re.IGNORECASE)

    used_datasets = use_pattern.findall(content_no_comments) + using_pattern.findall(content_no_comments)
    saved_datasets = save_pattern.findall(content_no_comments)

    entry_datasets = set(used_datasets) - set(saved_datasets)  # Removing output datasets from entry datasets

    reused_datasets = set(saved_datasets).intersection(used_datasets)
    not_reused_datasets = set(saved_datasets).difference(reused_datasets)

    print("Datasets Used as Entry (Excluding those also saved as output within the code):")
    for dataset in entry_datasets:
        print(f"* {dataset}")

    print("\nDatasets Produced and Reused:")
    for dataset in reused_datasets:
        print(f"* {dataset}")

    print("\nDatasets Produced but not Reused:")
    for dataset in not_reused_datasets:
        print(f"* {dataset}")

    if save_to_file:
        with open("output_datasets.txt", "w") as out_file:
            out_file.write("* Datasets Used as Entry (Excluding those also saved as output within the code):\n")
            for dataset in entry_datasets:
                out_file.write(f"* {dataset}\n")

            out_file.write("\n* Datasets Produced and Reused:\n")
            for dataset in reused_datasets:
                out_file.write(f"* {dataset}\n")

            out_file.write("\n* Datasets Produced but not Reused:\n")
            for dataset in not_reused_datasets:
                out_file.write(f"* {dataset}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract dataset information from a Stata do-file.')
    parser.add_argument('dofile', type=str, help='Path to the Stata do-file.')
    parser.add_argument('-s', '--save', action='store_true', help='Save output to output_datasets.txt file.')

    args = parser.parse_args()
    extract_datasets(args.dofile, args.save)
