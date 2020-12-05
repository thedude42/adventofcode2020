import sys
from collections import namedtuple

class Seat:
    '''
    "binary space partitioning" machine system for encoding airplane seating assignment...
    in the North Pole...
    '''
    def __init__(self, location: str, factor: int=8):
        self.encodedlocation = location
        self.rowfactor = factor

    @property
    def encodedlocation(self):
        return self.__encodedlocation

    @encodedlocation.setter
    def encodedlocation(self, location):
        self.__encodedlocation = location

    @property
    def rowfactor(self):
        return self.__rowfactor

    @rowfactor.setter
    def rowfactor(self, factor: int):
        self.__rowfactor = factor

    def binary_assign(self, rows: int=128, cols: int=8):
        col = 0
        row = 0
        col_stride = int(cols / 2)
        row_stride = int(rows / 2)
        for code in self.encodedlocation:
            if code in "FB":
                if code == "B":
                    row += row_stride
                row_stride = int(row_stride/ 2)
            if code in "LR":
                if code == "R":
                    col += col_stride
                col_stride = int(col_stride / 2)
        return row, col

    def get_seatid(self, row: int, col: int):
        return self.rowfactor * row + col

def get_seat_set(rowfactor: int=8, rows: int=128, cols: int=8):
    seats = set()
    for row in range(rows):
        for col in range(cols):
            seats.add(rowfactor * row + col)
    return seats

def main():
    if len(sys.argv) != 2:
        print("provide one parameter: filename for input")
        sys.exit(1)
    with open(sys.argv[1], 'r') as infile:
        seat_ids = []
        for line in infile:
            seat = Seat(line)
            seat_location = seat.binary_assign()
            seat_ids.append(seat.get_seatid(*seat_location))
    print ("Highest seat ID: {}".format(max(seat_ids)))
    occupied_seats = set(seat_ids)
    print("These seat IDs are empty: {}".format(get_seat_set() - occupied_seats))


if __name__ == '__main__':
    main()
