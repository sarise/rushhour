import sys
from collections import deque
from board import Board


class RushHour:
    def __init__(self, board):
        self.init_board = board

    def bfs(self, max_depth=25):
        '''
        Solve a Rush Hour game using breadth first search.
        :param max_depth: Maximum depth to traverse in search (default=25). To limit undesirable growth
        :return: a dict of results
        '''

        explored = set()
        solution = None
        depth_states = dict()

        q = deque()
        q.appendleft((self.init_board, tuple()))
        while len(q) != 0:
            board, path = q.pop()
            new_path = path + tuple([board])

            depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

            if len(new_path) >= max_depth:
                break

            hashed_board = hash(board)
            if hashed_board in explored:
                continue
            else:
                explored.add(hashed_board)

            if board.solved():
                solution = new_path
                break
            else:
                q.extendleft((move, new_path) for move in board.possible_moves())

        return {'solution': solution, 'depth_states': depth_states, 'explored': explored}

    def trace_path(self, solution):
        '''
        Translate a list of board states (solution) into car movements
        :param solution: a list of board states from initial to final position
        :return: a list or car movements
        '''
        steps = []
        for i in range(len(solution) - 1):
            car1 = list(solution[i].cars - solution[i + 1].cars)[0]
            car2 = list(solution[i + 1].cars - solution[i].cars)[0]

            if car1.x < car2.x:
                step = '{}-right'.format(car1.id)
            elif car1.x > car2.x:
                step = '{}-left'.format(car1.id)
            elif car1.y < car2.y:
                step = '{}-down'.format(car1.id)
            elif car1.y > car2.y:
                step = '{}-up'.format(car1.id)

            if step:
                steps.append(step)

        return steps

    def visualize(self, solution):
        '''
        Visualize the solution with state and its corresponding step
        :param solution:
        :return: None
        '''
        board = self.init_board

        print board,

        i = 0
        for move in solution:
            i += 1
            print '#{}: {}\n'.format(i, move)

            id, direction = move.split('-')
            car = board.get_car(id)
            if direction in ['right', 'down']:
                car_moved = board.forward(car)
            else:
                car_moved = board.reverse(car)

            board.cars.remove(car)
            board.cars.add(car_moved)
            board.refresh_grid()

            print board,


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input'
    game = RushHour(Board.from_file(filename))

    print "Rush Hour Game"
    print game.init_board

    res = game.bfs(max_depth=50)

    if res['solution'] > 0:
        print '\nSolution is found by exploring {:d} states.'.format(
            len(res['explored']))

        best_steps = game.trace_path(res['solution'])

        print 'It requires {:d} steps.'.format(len(best_steps))
        print ' '.join(best_steps) + '\n'

        game.visualize(best_steps)

    else:
        print 'I cannot solve the game.'
