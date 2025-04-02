class Tensor:
    def __init__(self, dimension: int | tuple, data: list):
        if not isinstance(dimension, (int, tuple)):
            raise TypeError("The valid type is int or tuple")
        else:
            if isinstance(dimension, int) and dimension <= 0:
                raise ValueError("The dimension must be greater than zero")
            else:
                for i in dimension:
                    if i <= 0:
                        raise ValueError("All dimensions must be greater than zero")

        self.data = data
        self.dimension = dimension

    def __repr__(self):
        return str(self.data)


class Matrix(Tensor):
    def __init__(self, dimension: tuple, data: list):
        if not isinstance(dimension, tuple):
            raise TypeError("The valid type is tuple")
        if len(dimension) != 2:
            raise ValueError("Tuple must be (rows, columns)")
        super().__init__(dimension, data)

    def conv_rc2i(self, row: int, column: int):
        rows, columns = self.dimension
        if row >= rows or -row < -rows:
            raise IndexError("Row index out of range")
        if column >= columns or -column < -columns:
            raise IndexError("Column index out of range")

        return (row % rows) * columns + column % columns

    def conv_i2rc(self, index):
        rows, columns = self.dimension
        if index >= rows * columns or -index < -rows * columns:
            raise IndexError("Index out of range")

        row = index % (rows * columns) // columns
        column = index % (rows * columns) % columns
        return row, column

    def __str__(self):
        if not self.data:
            return "[\n]"

        max_len_of_number = max(len(str(i)) for i in self.data)
        rows, columns = self.dimension

        result = "[\n"
        for i in range(rows - 1):
            row = "  ".join(f"{num:>{max_len_of_number}}" for num in self.data[i * columns:(i + 1) * columns])
            result += (row + "\n\n")
        row = "  ".join(f"{num:>{max_len_of_number}}" for num in self.data[(rows - 1) * columns:rows * columns])
        result += (row + "\n")
        result += "]"
        return result

    def __getitem__(self, key: int | list | slice | tuple):
        rows, columns = self.dimension

        if isinstance(key, int):
            if key >= rows or key < -rows:
                raise IndexError("Index is out of range")
            return Matrix((1, columns), self.data[(key % rows) * columns: (key % rows + 1) * columns])

        if isinstance(key, slice):
            all_rows = range(*key.indices(rows))
            new_data = []
            for row in all_rows:
                for i in self.data[row * columns: (row + 1) * columns]:
                    new_data.append(i)
            return Matrix((len(all_rows), columns), new_data)

        if isinstance(key, list):
            for i in key:
                if i >= rows or i < -rows:
                    raise IndexError("Index out of range")
            new_data = []
            for row in key:
                for i in self.data[row % rows * columns: (row % rows + 1) * columns]:
                    new_data.append(i)
            return Matrix((len(key), columns), new_data)

        if isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError("Tuple must have two elements")

            rows_key, columns_key = key
            all_columns = []
            all_rows = []

            if isinstance(columns_key, int) and isinstance(rows_key, int):
                if columns_key >= columns or columns_key < -columns:
                    raise IndexError("Index out of range")
                if rows_key >= rows or rows_key < -rows:
                    raise IndexError("Index out of range")
                return self.data[self.conv_rc2i(rows_key, columns_key)]

            if isinstance(columns_key, int):
                if columns_key >= columns or columns_key < -columns:
                    raise IndexError("Index out of range")
                all_columns = [columns_key]
            elif isinstance(columns_key, list):
                for i in columns_key:
                    if i >= rows or i < -rows:
                        raise IndexError("Index out of range")
                all_columns = columns_key.copy()
            elif isinstance(columns_key, slice):
                all_columns = list(range(*columns_key.indices(columns)))

            if isinstance(rows_key, int):
                if rows_key >= rows or rows_key < -rows:
                    raise IndexError("Index out of range")
                all_rows = [rows_key]
            elif isinstance(rows_key, list):
                for i in rows_key:
                    if i >= rows or i < -rows:
                        raise IndexError("Index out of range")
                all_rows = rows_key.copy()
            elif isinstance(rows_key, slice):
                all_rows = list(range(*rows_key.indices(rows)))

            new_data = []
            for row in all_rows:
                for column in all_columns:
                    new_data.append(self.data[self.conv_rc2i(row, column)])

            return Matrix((len(all_rows), len(all_columns)), new_data)


if __name__ == "__main__":
    M = Matrix((10, 10), list(range(100)))

    # print(M)
    # print(M[1, 1])
    # print(M[1])
    # print(M[-1])
    # print(M[1:4])
    # print(M[:4])
    # print(M[4:])
    # print(M[:])
    # print(M[1:7:2])
    # print(M[:, 1])
    # print(M[1:4, 1:4])
    # print(M[1:4, :4])
    # print(M[1:4, 4:])
    # print(M[1:4, :])
    # print(M[-1:])
    # print(M[-2::-2])
    # print(M[-2::-2, 1:4])
    # print(M[:, :])
    # print(M[[1, 4]])
    # print(M[:, [1, 4]])
    # print(M[[1, 4], [1, 4]])
