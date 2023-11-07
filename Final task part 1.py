import csv
import random
import os

def load_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data

def show(data, display_type='top', num_rows=5, separator=','):
    if display_type == 'top':
        display_data = data[:num_rows]
    elif display_type == 'bottom':
        display_data = data[-num_rows:]
    elif display_type == 'random':
        display_data = random.sample(data, num_rows)
    else:
        print("Недопустимый тип отображения. Пожалуйста, выберите один из 'top', 'bottom', или 'random'.")
        return

    for row in display_data:
        print(separator.join(row))

def info(data):
    num_rows = len(data) - 1  # Exclude header row
    num_columns = len(data[0])
    print(f"Количество строк: {num_rows}")
    print(f"Количество столбцов: {num_columns}")

    header = data[0]
    for i in range(num_columns):
        column_data = [row[i] for row in data[1:]]
        non_empty_values = [value for value in column_data if value != '']
        num_non_empty = len(non_empty_values)
        data_type = type(non_empty_values[0]).__name__ if num_non_empty > 0 else 'N/A'
        print(f"{header[i]}  {num_non_empty}  {data_type}")

def del_nan(data):
    cleaned_data = [row for row in data if all(value != '' for value in row)]
    return cleaned_data

def make_ds(filename):
    data = load_csv_file(filename)
    cleaned_data = del_nan(data)
    num_rows = len(cleaned_data)
    num_learning_rows = int(num_rows * 0.7)
    learning_data = cleaned_data[:num_learning_rows]
    testing_data = cleaned_data[num_learning_rows:]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    work_dir = os.path.join(base_dir, 'workdata')
    learning_dir = os.path.join(work_dir, 'Learning')
    testing_dir = os.path.join(work_dir, 'Testing')

    os.makedirs(learning_dir, exist_ok=True)
    os.makedirs(testing_dir, exist_ok=True)

    learning_filename = os.path.join(learning_dir, 'train.csv')
    testing_filename = os.path.join(testing_dir, 'test.csv')

    with open(learning_filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(learning_data)

    with open(testing_filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(testing_data)


filename = input("Введите имя json файла с его расширеним: ")
data = load_csv_file(filename)

show(data, display_type='top', num_rows=5, separator=',')
info(data)
cleaned_data = del_nan(data)
make_ds(filename)