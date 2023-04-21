import os
import csv
import re
from datetime import datetime

def extract_date(filename):
    date_pattern = r'\d{4}_\d{2}_\d{2}-\d{2}_\d{2}_\d{2}'
    match = re.search(date_pattern, filename)
    if match:
        return datetime.strptime(match.group(), '%Y_%m_%d-%H_%M_%S').strftime('%Y_%m_%d_%H_%M_%S')
    else:
        raise ValueError(f"Date not found in filename: {filename}")

# fix simostools special characters for winOS users
def sanitize_filename(filename, replace_with="_"):
    invalid_chars = r'[<>:"/\|?*]'
    sanitized = re.sub(invalid_chars, replace_with, filename)
    max_length = 255
    return sanitized[:max_length]

def rename_csv_files(folder_path, cell_row, cell_col):
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    for i, row in enumerate(reader):
                        if i == cell_row:
                            num_columns = len(row)
                            if cell_col < num_columns:
                                cell_value = row[cell_col]
                            else:
                                print(f"Column index {cell_col} is out of range for file {file} (total columns: {num_columns}). Skipping.")
                                continue
                            break
                    
                # debug 
                # print(f"Number of columns in file {file}: {num_columns}")

                date = extract_date(file)
                new_filename = f"{cell_value}_{date}.csv"
                new_filename = sanitize_filename(new_filename)

                # Remove the "simostools" from the new file name
                new_filename = new_filename[11:]

                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed {file} to {new_filename}")

            except Exception as e:
                print(f"Error processing file {file}: {e}")

if __name__ == "__main__":
    folder_path = "logs"
    cell_row = 0  # Row index of the cell
    cell_col = 82  # Column index of the cell

    rename_csv_files(folder_path, cell_row, cell_col)
