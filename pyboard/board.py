from typing import Tuple, Union


class Board(dict):
    class Subset:
        def __init__(self, board, coordinate_generator):
            self.board = board
            self.coordinate_generator = coordinate_generator

        def iterator(self, *args, **kwargs):
            for item in self.coordinate_generator(*args, **kwargs):
                print(item, self.board[item])
                yield self.board[item]

    class Row(Subset):
        def __init__(self, board, row):
            # Define generator function, using yield for lazy evaluation
            def gen(start=0, stop=None):
                for col in range(0 if stop is None else start, board.rows if stop is None else stop):
                    yield row, col
            # Pass generator function through to Subset
            super().__init__(board, gen)
            self.board = board
            self.row = row

        def __iter__(self):
            return self.iterator()

        def __getitem__(self, item):
            return self.board[(self.row, item)]

        def __setitem__(self, col, value):
            self.board[(self.row, col)] = value

        def __delitem__(self, col):
            del self.board[(self.row, col)]

    class Column(Subset):
        def __init__(self, board, col):
            # Define generator function, using yield for lazy evaluation
            def gen(start=0, stop=None):
                for row in range(0 if stop is None else start, board.cols if stop is None else stop):
                    yield row, col
            # Pass generator function through to Subset
            super().__init__(board, gen)
            self.board = board
            self.col = col

        def __iter__(self):
            return self.iterator()

        def __getitem__(self, item):
            return self.board[(item, self.col)]

        def __setitem__(self, row, value):
            self.board[(row, self.col)] = value

        def __delitem__(self, row):
            del self.board[(row, self.col)]

    def __init__(self, arg: "Union[Board, Tuple[int, int]]"):
        super().__init__()
        if isinstance(arg, Board):
            self.rows = arg.rows
            self.cols = arg.cols
            for k, v in arg.items():
                self[k] = v
        elif isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], int) and isinstance(arg[1], int):
            self.rows = arg[0]
            self.cols = arg[1]

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.Row(self, item)
        return super().__getitem__(item) if item in self else None

    def __setitem__(self, key, value):
        if not (isinstance(key, tuple) and len(key) == 2):
            raise ValueError(
                "{} keys must be Tuple[int, int], not {}".format(
                    type(self).__name__,
                    type(key).__name__
                )
            )
        super().__setitem__(key, value)

    def values(self):
        def gen():
            for row in range(self.rows):
                for col in range(self.cols):
                    yield row, col
        return Board.Subset(self, gen)

    def row(self, row):
        return self.Row(self, row)

    def col(self, col):
        return self.Column(self, col)

    def __repr__(self):
        lines = []
        divider = '+' + '---+' * self.cols
        lines.append(divider)
        for row in range(self.rows):
            line = '|'
            for col in range(self.cols):
                value = self[row][col]
                line += ' {} |'.format(value if value else '-')
            lines.append(line)
            lines.append(divider)
        return '\n'.join(lines)


if __name__ == '__main__':
    b = Board((9, 9))
    print("All Columns")
    [None for item in b.row(0)]
    print("Columns 1-4")
    [None for item in b.row(0).iterator(1, 5)]
    print("All Rows")
    [None for item in b.col(0)]
    print("Rows 1-4")
    [None for item in b.col(0).iterator(1, 5)]
    print(b)
