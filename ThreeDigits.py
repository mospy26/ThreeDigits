import sys

class State:
	def __init__(self, state, parent = None, heuristic = 0):
		self.state = state
		self.parent = parent
		self.heuristic = heuristic
		self.children = []

	def __repr__(self):
		return self.state

	def __eq__(self, other):
		return self.state == other.state and self.children == other.children and self.parent.state == other.parent.state

	def next(self, direction, arithmetic = "sub"):
		if (self.state[0], direction, arithmetic) in [("0", 2, "sub"),("9", 2, "add")] or \
			(self.state[1], direction, arithmetic) in [("0", 1, "sub"),("9", 1, "add")] or \
			(self.state[2], direction, arithmetic) in [("0", 0, "sub"),("9", 0, "add")]:
				return None
		return State(str(int(self.state) + pow(10,direction)).zfill(3), self, 0) if arithmetic is "add" else \
			State(str(int(self.state) - pow(10,direction)).zfill(3), self, 0)

	def last_changed_digit(self):
		if int(self.parent.state) - int(self.state) in [-100, 100]:
			return 2
		if int(self.parent.state) - int(self.state) in [-10, 10]:
			return 1
		if int(self.parent.state) - int(self.state) in [-1, 1]:
			return 0

	def generate_children(self):
		digit_list = [2,1,0]
		if self.parent is not None:
			digit_list.remove(self.last_changed_digit())

		for i in digit_list:
			child = self.next(i)
			if child is not None:
				self.children.append(child)

			child = self.next(i, "add")
			if child is not None:
				self.children.append(child)
		return

class ThreeDigitsSolver:

	def __init__(self, start_state, end_state, forbidden_states, algorithm):
		self.start_state = State(start_state)
		self.end_state = State(end_state)
		self.algorithm = algorithm
		self.forbidden_states = forbidden_states
		self.result = [["No solution Found"], []]

	def solve(self):
		self.algorithms[self.algorithm](self)

	def print_result(self):
		print(repr(self.result[0])[1:-1] + "\n" + repr(self.result[1])[1:-1])

	def BFS(self):
		seen = [self.start_state]
		visited = [self.start_state]

		expanded = []

		while len(seen) != 0 and len(expanded) <= 1000:
			current_state = seen.pop(0)
			current_state.generate_children()
			expanded.append(current_state)

			if self.end_state.state == current_state.state:
				self.result[0].clear()
				self.result[1] = expanded
				st = current_state
				while st is not None:
					self.result[0].append(st)
					st = st.parent
				self.result[0].reverse()
				return

			for state in current_state.children:
				is_forbidden = False if self.forbidden_states is None else state in self.forbidden_states
				if state not in visited and not is_forbidden:
					seen.append(state)
					visited.append(state)

		self.result[1] = expanded
		return


	def DFS(self):
		pass

	def IDS(self):
		pass

	def greedy(self):
		pass

	def a_star(self):
		pass

	def hill_climbing(self):
		pass

	algorithms = { \
		"B" : BFS, \
		"D" : DFS, \
		"I" : IDS, \
		"G" : greedy, \
		"A" : a_star, \
		"H" : hill_climbing
	}

def main():
	try:
		algorithm = sys.argv[1]
		if algorithm not in ["B", "D", "I","G", "A", "H"]:
			raise ValueError("No algorithm is a acronym for the specified argument " + algorithm)
	except:
		sys.exit(-1)

	file = sys.argv[2]
	try:
		with open(file) as f:
			lines = f.readlines()
			lines = [line.strip() for line in lines]
	except:
		sys.exit(-1)

	solver = None
	try:
		forbidden = lines[2].split(",")
		forbidden_states = [State(state, None, 0) for state in forbidden]
		solver = ThreeDigitsSolver(lines[0], lines[1], forbidden_states[:], algorithm)
	except:
		solver = ThreeDigitsSolver(lines[0], lines[1], None, algorithm)

	solver.solve()
	solver.print_result()
	return

if __name__ == "__main__":
	main()
