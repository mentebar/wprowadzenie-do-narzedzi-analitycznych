import random

def read_data(filepath: str, header=True, delimiter=',', encoding="utf-8"):
    """
    :param filepath: ścieżka do pliku z danymi
    :param header: czy w pierwszej linii pliku z danymi znajdują się nazwy kolumn (etykiety kolumn)
    :param delimiter: ogranicznik pola w pliku z danymi, separator, który oddziela dane w wierszu
    :param encoding: kodowanie pliku, domyślnie UTF-8
    :return: etykiety oraz dane
    """
    labels = []
    data = []

    try:
        with open(filepath, encoding=encoding) as filehandler:
            for line_idx, line in enumerate(filehandler):
                clean_line = line.strip().split(delimiter) 
                if line_idx == 0 and header:
                    labels = clean_line 
                else:
                    data.append(clean_line)
    except IOError as err:
        print(f"Błąd odczytu pliku z danymi: {err}")

    return labels, data

def print_labels(labels):
    """
    Funkcja wypisuje nazwy kolumn zbioru danych.
    """
    print('Zbiór danych zawiera następujące kolumny:')
    print(", ".join(labels)) 

def get_number_of_classes(data, class_col_index=-1):
    """
    Funkcja zwraca liczbę klas decyzyjnych.
    """
    class_counts = {}

    for row in data:
        if class_col_index < len(row): 
            class_name = row[class_col_index]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

    return list(class_counts.items())

def data_split(data, train_pct=0.7, test_pct=0.3, val_pct=0.0):
    """
    Funkcja dzieli dane na zbiory: treningowy, testowy i walidacyjny.
    """
    total_pct = train_pct + test_pct + val_pct
    if round(total_pct, 5) != 1.0: 
        raise ValueError("Suma wartości procentowych musi wynosić 1!")

    random.shuffle(data)

    train_last_index = int(len(data) * train_pct)
    test_last_index = int(len(data) * (train_pct + test_pct))

    train_data = data[:train_last_index]
    test_data = data[train_last_index:test_last_index]
    valid_data = data[test_last_index:]

    return train_data, test_data, valid_data

if __name__ == "__main__":
    labels, data = read_data('diabetes.csv')
    print_labels(labels)

    print(get_number_of_classes(data))

    for subset in data_split(data):
        print(f"Ilość elementów w zbiorze: {len(subset)}")

    for subset in data_split(data, 0.7, 0.2, 0.1):
        print(f"Ilość elementów w zbiorze: {len(subset)}")

    for subset in data_split(data, 0.8, 0.1, 0.1):
        print(f"Ilość elementów w zbiorze: {len(subset)}")
