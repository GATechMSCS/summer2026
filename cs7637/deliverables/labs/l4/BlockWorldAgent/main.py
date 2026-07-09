from BlockWorldAgent import BlockWorldAgent

def test():
    #This will test your BlockWorldAgent
	#with eight initial test cases.
    test_agent = BlockWorldAgent()

    initial_arrangement_1 = [["A", "B", "C"], ["D", "E"]]
    goal_arrangement_1 = [["A", "C"], ["D", "E", "B"]]
    goal_arrangement_2 = [["A", "B", "C", "D", "E"]]
    goal_arrangement_3 = [["D", "E", "A", "B", "C"]]
    goal_arrangement_4 = [["C", "D"], ["E", "A", "B"]]

    print(f"Initial Arrangement 1: {initial_arrangement_1}")
    print(f"Goal Arrangement 1: {goal_arrangement_1}")
    print(f"Solve 1: {test_agent.solve(initial_arrangement_1, goal_arrangement_1)}")
    print(f"Goal Arrangement 2: {goal_arrangement_2}")
    print(f"Solve 2: {test_agent.solve(initial_arrangement_1, goal_arrangement_2)}")
    print(f"Goal Arrangement 3: {goal_arrangement_3}")
    print(f"Solve 3: {test_agent.solve(initial_arrangement_1, goal_arrangement_3)}")
    print(f"Goal Arrangement 4: {goal_arrangement_4}")
    print(f"Solve 4: {test_agent.solve(initial_arrangement_1, goal_arrangement_4)}")

    initial_arrangement_2 = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
    goal_arrangement_5 = [["A", "B", "C", "D", "E", "F", "G", "H", "I"]]
    goal_arrangement_6 = [["I", "H", "G", "F", "E", "D", "C", "B", "A"]]
    goal_arrangement_7 = [["H", "E", "F", "A", "C"], ["B", "D"], ["G", "I"]]
    goal_arrangement_8 = [["F", "D", "C", "I", "G", "A"], ["B", "E", "H"]]

    print(f"\nInitial Arrangement 2: {initial_arrangement_2}")
    print(f"Goal Arrangement 5: {goal_arrangement_5}")
    print(f"Solve 5: {test_agent.solve(initial_arrangement_2, goal_arrangement_5)}")
    print(f"Goal Arrangement 6: {goal_arrangement_6}")
    print(f"Solve 6: {test_agent.solve(initial_arrangement_2, goal_arrangement_6)}")
    print(f"Goal Arrangement 7: {goal_arrangement_7}")
    print(f"Solve 7: {test_agent.solve(initial_arrangement_2, goal_arrangement_7)}")
    print(f"Goal Arrangement 8: {goal_arrangement_8}")
    print(f"Solve 8: {test_agent.solve(initial_arrangement_2, goal_arrangement_8)}")

if __name__ == "__main__":
    test()