import os
import hashlib
import csv
from collections import defaultdict

def get_file_hash(file_path):
   """Generate a hash for a file, but skip anything larger than 100MB."""
   file_size = os.path.getsize(file_path)
   if file_size > 100 * 1024 * 1024: # 100MB in bytes or 104,857,600 bytes
       return None # Skip the file
   
   hasher = hashlib.md5()
   with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        return hasher.hexdigest()

def sort_files(directory):
    """Recursively sort files in a directory by name."""
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    file_list.sort()
    return file_list

def find_duplicates(directory):
    """Recursively find duplicate files in a directories.  This compares actual file contents and not just file names. It will find files that are identical but differently named i.e. file(1).pdf and file.pdf"""
    hash_map = defaultdict(list)
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                file_hash = get_file_hash(file_path)
                hash_map[file_hash].append(file_path)
    
    duplicates = {hash: paths for hash, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def write_to_csv(file_list, csv_path):
    # The file must not exist. If you want to append, change the 'w' to 'a' in the "open" statement.
    # Writes the file path, file name, and file hash for later sorting against duplicates in other folders.
    """Write the list of files to a CSV file."""
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File Path', 'File Name', 'File Hash'])
        for file in file_list:
            csvwriter.writerow([os.path.dirname(file), os.path.basename(file), get_file_hash(file)])

def main():
    directory = 'c:\\temp\\input'
    csv_path = 'c:\\temp\\output\\output.csv'

    # Get and print sorted files
    sorted_files = sort_files(directory)
    print("Sorted files:", sorted_files)

    # Find and print duplicates
    duplicates = find_duplicates(directory)
    if duplicates:
        print("Duplicate files found:")
        for file_hash, paths in duplicates.items():
            print(f"Hash: {file_hash}")
            for path in paths:
                print(f" - {path}")
    else:
        print("No duplicate files found.")

    # Write sorted files to CSV
    write_to_csv(sorted_files, csv_path)
    print(f"File list written to {csv_path}")

if __name__ == "__main__":
    main()
