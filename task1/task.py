import csv

i = 5
j = 3

with open('file.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)

    for _ in range(i - 1):
        next(csvreader)
    
    row = next(csvreader)
    element = row[j - 1]

    print(f'На позиции ({i}, {j}): {element}')
