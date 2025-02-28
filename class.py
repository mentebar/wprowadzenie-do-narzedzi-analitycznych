import random


class Dataset:
    def __init__(self):
        self.data = []
        self.labels = []
        self.class_column_index = None

    def read_data(self, filepath: str, header=True, delimiter=',', class_col_index=-1, encoding="utf-8"):
        self.class_column_index = class_col_index
        try:
            with open(filepath, encoding=encoding) as filehandler:
                for line_idx, line in enumerate(filehandler):
                    clean_line = line.strip().split(delimiter) 
                    if line_idx == 0 and header:
                        self.labels = clean_line
                    else:
                        self.data.append(clean_line)
        except IOError as err:
            print(f"Błąd odczytu pliku z danymi: {err}")

    def get_labels(self) -> list[str]:
        return self.labels

    def get_number_of_classes(self):
        class_counts = {}
        for row in self.data:
            class_name = row[self.class_column_index]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        return [(key, value) for key, value in class_counts.items()]

    def data_split(self, train_pct=0.7, test_pct=0.3, val_pct=0.0):
        if not (0 <= train_pct <= 1 and 0 <= test_pct <= 1 and 0 <= val_pct <= 1):
            raise ValueError("Procenty muszą być w zakresie 0-1")
        if round(train_pct + test_pct + val_pct, 5) != 1:
            raise ValueError("Suma podziałów musi wynosić 1")

        random.shuffle(self.data)
        train_last_index = int(len(self.data) * train_pct)
        test_last_index = int(len(self.data) * (train_pct + test_pct))

        train_data = self.data[:train_last_index]
        test_data = self.data[train_last_index:test_last_index]
        valid_data = self.data[test_last_index:]

        return train_data, test_data, valid_data


if __name__ == "__main__":
    ds = Dataset()
    ds.read_data('diabetes.csv')
    print(ds.get_labels())
    print(ds.labels)
    print(ds.data)
    print(ds.get_number_of_classes())

    for subset in ds.data_split():
        print(f"Ilość elementów w zbiorze: {len(subset)}")

    for subset in ds.data_split(0.7, 0.2, 0.1):
        print(f"Ilość elementów w zbiorze: {len(subset)}")

    for subset in ds.data_split(0.8, 0.1, 0.1):
        print(f"Ilość elementów w zbiorze: {len(subset)}")
