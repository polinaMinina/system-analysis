import io
import csv
import numpy as np

def csv_file_to_string(file_path: str) -> str:
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = [row for row in reader]
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerows(rows)
    
    return output.getvalue().strip()

csv_file_path = "./task3.csv"
csv_string = csv_file_to_string(csv_file_path)


def task(csv_string: str) -> float:
    f = io.StringIO(csv_string)
    reader = csv.reader(f, delimiter=';')
    matrix = np.array([[int(num) for num in row] for row in reader])
    
    n, k = matrix.shape

    entropy = 0
    for j in range(n):
        for i in range(k):
            l_ij = matrix[j, i]
            if l_ij != 0: 
                entropy -= (l_ij / (n - 1)) * np.log2(l_ij / (n - 1))

    return round(entropy, 1)


print(task(csv_string))
