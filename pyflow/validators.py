import csv
import os
from utils import ValidationError

def validate_csv_structure(file_path: str, encoding: str, error_file: str) -> int:
    bad_rows = []
    
    with open(file_path, newline="", encoding=encoding) as f:
        reader = csv.reader(f)
        
        try:
            header = next(reader)
            expected_columns = len(header)

            if not header:
                raise ValidationError(f"CSV file contains no header: {file_path}")
        
        except StopIteration:
            raise ValidationError(f"CSV file contains no data: {file_path}")

        for line_number, row in enumerate(reader, start=2):
            if len(row) != expected_columns:
                bad_rows.append((line_number, row))
        
        if bad_rows:        
            with open(error_file, "w", encoding=encoding) as error_log:
                error_log.write("line_number, row\n")

                for line_number, row in bad_rows:
                        error_log.write(f"{line_number}, {row}\n")
    
    return len(bad_rows)