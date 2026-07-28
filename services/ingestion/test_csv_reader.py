from config import DATASET_FOLDER
from csv_reader import CSVReader

reader = CSVReader(DATASET_FOLDER)

for file_name, chunk, row_number, row in reader.read_rows():

    print(file_name)
    print(chunk)
    print(row_number)
    print(row)

    break