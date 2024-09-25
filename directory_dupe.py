import os
import hashlib
import csv
from collections import defaultdict

def get_file_hash(file_path):
    """Generate a hash for a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def sort_files(directory):
    """Sort files in a directory by name."""
    files = os.listdir(directory)
    files.sort()
    return files

def find_duplicates(directory):
    """Find duplicate files in a directory."""
    files = os.listdir(directory)
    hash_map = defaultdict(list)

    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path)
            hash_map[file_hash].append(file_path)

    duplicates = {hash: paths for hash, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def write_to_csv(file_list, csv_path):
    """Write the list of files to a CSV file."""
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Path', 'File Name'])
        for file in file_list:
            csvwriter.writerow([os.path.realpath(file), file])

def main():
    directory = 'c:\\drivers'
    csv_path = 'c:\\temp\output\output.csv'
    sorted_files = sort_files(directory)
    print("Sorted files:", sorted_files)
    duplicates = find_duplicates(directory)
    if duplicates:
        print("Duplicate files found:")
        for file_hash, paths in duplicates.items():
            print(f"Hash: {file_hash}")
            for path in paths:
                print(f" - {path}")
    else:
        print("No duplicate files found.")

    write_to_csv(sorted_files, csv_path)
    print(f"File list written to {csv_path}")

if __name__ == "__main__":
    main()