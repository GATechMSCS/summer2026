class BlockWorldAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        #Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")

        legal_moves = []
        block_below = {}
        block_above = {}
        goal_block_below = {}

        for group in initial_arrangement:
            for idx, block in enumerate(group):

                if idx == 0:
                    block_below[block] = "Table"

                else:
                    block_below[block] = group[idx - 1]
                    block_above[group[idx - 1]] = block

                if block not in block_above:
                    block_above[block] = None

        for group in goal_arrangement:
            for idx, block in enumerate(group):

                if idx == 0:
                    goal_block_below[block] = "Table"

                else:
                    goal_block_below[block] = group[idx - 1]

        bottom_blocks = []
        tops_blocks = []

        for group in goal_arrangement:
            for block in group:
                if goal_block_below[block] == "Table":
                    bottom_blocks.append(block)
                else:
                    tops_blocks.append(block)

        for block in bottom_blocks + tops_blocks:
                if self._final_position(block, goal_block_below, block_below):
                    continue

                self._clear_block_above(block, block_above, block_below, legal_moves, goal_block_below)
                target_block = goal_block_below[block]

                if target_block != "Table":
                    self._clear_block_above(target_block, block_above, block_below, legal_moves, goal_block_below)

                if block_below[block] != target_block:
                    self._move_block(block, target_block, block_above, block_below, legal_moves)

        return legal_moves

    def _final_position(self, block, goal_block_below, block_below):

        curr = block
        while True:

            target_block = goal_block_below[curr]

            if block_below[curr] != target_block:
                return False

            if target_block == "Table":
                return True

            curr = target_block

    def _clear_block_above(self, block, block_above, block_below, legal_moves, goal_block_below):

        while block_above[block] is not None:
            top_block = block_above[block]

            if block_above[top_block] is not None:
                self._clear_block_above(top_block, block_above, block_below, legal_moves, goal_block_below)

            dest = "Table"
            if top_block in goal_block_below:
                below_at_goal = goal_block_below[top_block]
                if below_at_goal != "Table":
                    if block_above[below_at_goal] is None and \
                       self._final_position(below_at_goal, goal_block_below, block_below):
                           dest = below_at_goal

            self._move_block(top_block, dest, block_above, block_below, legal_moves)

    def _move_block(self, block, dest, block_above, block_below, legal_moves):

        prev_block_below = block_below[block]
        block_below[block] = dest

        if prev_block_below != "Table":
            block_above[prev_block_below] = None

        if dest != "Table":
            block_above[dest] = block

        legal_moves.append((block, dest))
