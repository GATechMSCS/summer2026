class SemanticNetsAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        self.legal_moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        self.boat_goal = (0, 0, 1)

    def solve(self, initial_sheep, initial_wolves):
        #Add your code here! Your solve method should receive
        #the initial number of sheep and wolves as integers,
        #and return a list of 2-tuples that represent the moves
        #required to get all sheep and wolves from the left
        #side of the river to the right.
        #
        #If it is impossible to move the animals over according
        #to the rules of the problem, return an empty list of
        #moves.

        swb_start_states = (initial_sheep, initial_wolves, 0)
        to_visit = [(swb_start_states, [])]
        visited = {swb_start_states}

        while to_visit:

            swb_states, boat_path = to_visit.pop(0)
            sheep_left_side, wolves_left_side, boat_side = swb_states

            if swb_states == self.boat_goal:
                return boat_path

            for sheep_moves, wolf_moves in self.legal_moves:

                if boat_side == 0:
                    new_left_sheep = sheep_left_side - sheep_moves
                    new_left_wolves = wolves_left_side - wolf_moves
                    next_boat_side = 1

                else:
                    new_left_sheep = sheep_left_side + sheep_moves
                    new_left_wolves = wolves_left_side + wolf_moves
                    next_boat_side = 0

                sheep_right_side = initial_sheep - new_left_sheep
                wolves_right_side = initial_wolves - new_left_wolves

                if new_left_sheep < 0 or new_left_wolves < 0:
                    continue
                if sheep_right_side < 0 or wolves_right_side < 0:
                    continue
                if new_left_sheep > 0 and new_left_wolves > new_left_sheep:
                    continue
                if sheep_right_side > 0 and wolves_right_side > sheep_right_side:
                    continue

                next_state = (new_left_sheep, new_left_wolves, next_boat_side)

                if next_state not in visited:
                    visited.add(next_state)
                    to_visit.append((next_state, boat_path + [(sheep_moves, wolf_moves)]))
        return []


