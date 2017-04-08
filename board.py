from car import Car


class Board(object):

    EMPTY = '.'
    RED_CAR_FINAL_POSITION = Car('r', 4, 2, '-', 2)

    def __init__(self, vehicles, grid_size = (6, 6)):
        self.cars = vehicles
        self.grid_size = grid_size
        self.refresh_grid()

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.cars == other.cars

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        s = ''
        for line in self.grid:
            s += ''.join(line) + '\n'
        return s.rstrip()

    def refresh_grid(self):
        '''
        Refresh the board state, possibly because a car has moved
        :return: new Rush Hour board state
        '''
        self.grid = self.get_array()

    def get_car(self, id):
        '''
        Get the instance of car based on its id
        :param id: car id
        :return: an instance of car
        '''
        for car in self.cars:
            if car.id == id:
                return car

    def get_array(self):
        '''
        Translate a list of car locations into a grid
        :return: the state of a Rush Hour board
        '''
        board = [[Board.EMPTY] * self.grid_size[1] for i in range(self.grid_size[0])]
        for car in self.cars:
            x, y = car.x, car.y
            if car.orientation == '-':
                for i in range(car.length):
                    board[y][x + i] = car.id
            else:
                for i in range(car.length):
                    board[y + i][x] = car.id
        return board

    def solved(self):
        '''
        Check whether the red car has reaches the final position near the exit
        :return: boolean flag
        '''
        return Board.RED_CAR_FINAL_POSITION in self.cars

    def reverse(self, car):
        '''
        With a given board state, move the specified car backward
        :param car: the car to be moved
        :return: an instance of car with new position
        '''
        x, y = car.x, car.y
        if car.orientation == '-':
            new_x = x - 1
            if x - 1 >= 0 and self.grid[y][new_x] == Board.EMPTY:
                return Car(car.id, new_x, y, car.orientation, car.length)

        else:
            new_y = y - 1
            if new_y >= 0 and self.grid[new_y][x] == Board.EMPTY:
                return Car(car.id, x, new_y, car.orientation, car.length)

    def forward(self, car):
        '''
        With a given board state, move the specified car forward
        :param car: the car to be moved
        :return: an instance of car with new position
        '''
        x, y = car.x, car.y
        if car.orientation == '-':
            if x + car.length < self.grid_size[1] and self.grid[y][x + car.length] == Board.EMPTY:
                return Car(car.id, x + 1, y, car.orientation, car.length)

        else:
            if y + car.length < self.grid_size[1] and self.grid[y + car.length][x] == Board.EMPTY:
                return Car(car.id, x, y + 1, car.orientation, car.length)

    def possible_moves(self):
        '''
        Generate an iterator of every possible board states after a car moves forward or reverse
        :return: an iterator of board states
        '''
        for car in self.cars:
            moved = self.forward(car)
            if moved:
                new_cars = self.cars.copy()
                new_cars.remove(car)
                new_cars.add(moved)
                yield Board(new_cars)

            moved = self.reverse(car)
            if moved:
                new_cars = self.cars.copy()
                new_cars.remove(car)
                new_cars.add(moved)
                yield Board(new_cars)

    @classmethod
    def from_file(cls, filename):
        '''
        Instantiate a Rush Hour board from a given file with certain format.

        :param filename: a file contains the initial state of Rush Hour board
        :return: an instance of Rush Hour board
        '''
        with open(filename) as f:
            state = [s.rstrip() for s in f.readlines()]

        cars = []
        y = 0
        while y < len(state):
            x = 0
            while x < len(state[y]):
                if state[y][x] != Board.EMPTY:
                    if x+1 < len(state[y]) and state[y][x] == state[y][x+1]:
                        length = 2
                        while x+length < len(state[y]) and state[y][x] == state[y][x+length]:
                            length += 1
                        cars.append(Car(state[y][x], x, y, '-', length))
                        x += length - 1
                    elif y-1 > 0 and state[y][x] == state[y-1][x]:
                        pass
                    elif y+1 < len(state) and state[y][x] == state[y+1][x]:
                        length = 2
                        while y+length < len(state) and state[y][x] == state[y+length][x]:
                            length +=1
                        cars.append(Car(state[y][x], x, y, '|', length))
                x += 1
            y += 1
        return cls(set(cars))


