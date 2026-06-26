from SemanticNetsAgent import SemanticNetsAgent

def test():
    #This will test your SemanticNetsAgent
	#with seven initial test cases.
    test_agent = SemanticNetsAgent()

    print("input: (1, 1)", "output: ", test_agent.solve(1, 1))
    print("input: (2, 2)", "output: ", test_agent.solve(2, 2))
    print("input: (3, 3)", "output: ", test_agent.solve(3, 3))
    print("input: (5, 3)", "output: ", test_agent.solve(5, 3))
    print("input: (6, 3)", "output: ", test_agent.solve(6, 3))
    print("input: (7, 3)", "output: ", test_agent.solve(7, 3))
    print("input: (5, 5)", "output: ", test_agent.solve(5, 5))

if __name__ == "__main__":
    test()